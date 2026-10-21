import json
import os
import uuid

from flask import Blueprint, current_app, g, jsonify, request
from google.cloud import firestore

from adapters.paystack import initialize_transaction, mock_initialize_transaction, verify_signature
from adapters.registry import build_adapters

from .. import sender, wallet
from ..audit import append_event
from ..auth import require_auth
from ..db import get_db, tenant_ref

bp = Blueprint("money", __name__)


def _adapters():
    return current_app.config.get("ADAPTERS") or build_adapters(current_app.config["SETTINGS"])


def _link_fn():
    fn = current_app.config.get("PAYMENT_LINK_FN")
    if fn:
        return fn
    return mock_initialize_transaction if os.getenv("PAYSTACK_MOCK") == "true" else initialize_transaction


@bp.get("/v1/wallet")
@require_auth()
def get_wallet():
    q = tenant_ref(g.tenant_id).collection("wallet_ledger").order_by(
        "at", direction=firestore.Query.DESCENDING).limit(20)
    entries = [{**{k: v for k, v in d.to_dict().items() if k != "at"},
                "at": d.to_dict()["at"].isoformat()} for d in q.stream()]
    return jsonify(balance_kobo=wallet.balance(g.tenant_id), entries=entries)


@bp.post("/v1/wallet/topup")
@require_auth("admin")
def topup():
    amount = (request.get_json(silent=True) or {}).get("amount_naira")
    if not isinstance(amount, (int, float)) or amount < 100:
        return jsonify(error="amount_naira must be at least 100"), 400
    reference = f"es-topup-{uuid.uuid4().hex}"
    get_db().collection("payment_refs").document(reference).set({
        "tenant_id": g.tenant_id, "purpose": "wallet_topup", "expected_kobo": int(round(amount * 100))})
    try:
        link = _link_fn()(g.email or "billing@example.com", amount, reference, {"tenant_id": g.tenant_id})
    except Exception:
        return jsonify(error="Could not create the payment link"), 502
    return jsonify(reference=reference, payment_url=link["authorization_url"])


@bp.post("/v1/batches/<batch_id>/send")
@require_auth("checker", "admin")
def send_batch(batch_id):
    s = current_app.config["SETTINGS"]
    out = sender.process_batch(g.tenant_id, batch_id, _adapters(), _link_fn(),
                               s.message_price_kobo, s.first_notice_channels)
    if out["result"] == "not_found":
        return jsonify(error="Batch not found"), 404
    if out["result"] == "bad_status":
        return jsonify(error="Only an approved batch can be sent"), 409
    if out["result"] == "busy":
        return jsonify(error="This batch is already being sent"), 409
    append_event(g.tenant_id, g.uid, "batch_send_run", {"batch_id": batch_id, **out})
    return jsonify(out)


@bp.post("/v1/suppressions")
@require_auth("maker", "checker", "admin")
def add_suppression():
    contact = ((request.get_json(silent=True) or {}).get("contact") or "").strip()
    if not contact:
        return jsonify(error="contact is required"), 400
    contact = contact.lower() if "@" in contact else contact.replace("+", "").replace(" ", "")
    tenant_ref(g.tenant_id).collection("suppressions").document(sender.contact_hash(contact)).set(
        {"at": firestore.SERVER_TIMESTAMP, "by": g.uid})
    append_event(g.tenant_id, g.uid, "opt_out_recorded", {"contact_sha256": sender.contact_hash(contact)})
    return jsonify(status="recorded")


@bp.get("/v1/dashboard")
@require_auth()
def dashboard():
    t = {"sent_count": 0, "sent_kobo": 0, "paid_count": 0, "paid_kobo": 0,
         "failed_count": 0, "mismatch_count": 0}
    for b in tenant_ref(g.tenant_id).collection("batches").stream():
        d = b.to_dict()
        for k in t:
            t[k] += d.get(k, 0)
    return jsonify(**t, outstanding_kobo=t["sent_kobo"] - t["paid_kobo"],
                   wallet_kobo=wallet.balance(g.tenant_id))


@firestore.transactional
def _match(txn, pref, rref, bref, paid, currency, reference):
    if pref.get(transaction=txn).exists:
        return "duplicate"
    rsnap = rref.get(transaction=txn)
    if not rsnap.exists:
        return "unmatched"
    expected = rsnap.get("amount_kobo")
    ok = paid == expected and currency == "NGN"
    txn.set(pref, {"reference": reference, "paid_kobo": paid, "expected_kobo": expected,
                   "currency": currency, "status": "matched" if ok else "mismatch",
                   "at": firestore.SERVER_TIMESTAMP})
    txn.update(rref, {"status": "paid" if ok else "paid_mismatch", "paid_kobo": paid})
    txn.update(bref, {"paid_count": firestore.Increment(1), "paid_kobo": firestore.Increment(paid)}
               if ok else {"mismatch_count": firestore.Increment(1)})
    return "matched" if ok else "mismatch"


@bp.post("/webhooks/paystack")
def paystack_webhook():
    secret = os.getenv("PAYSTACK_SECRET_KEY", "")
    raw = request.get_data()
    if not secret or not verify_signature(secret, raw, request.headers.get("X-Paystack-Signature", "")):
        return jsonify(error="Bad signature"), 401
    event = json.loads(raw)
    if event.get("event") != "charge.success":
        return jsonify(status="ignored")
    data = event["data"]
    reference, paid, currency = data["reference"], int(data["amount"]), data.get("currency", "NGN")

    ref_doc = get_db().collection("payment_refs").document(reference).get()
    if not ref_doc.exists:
        get_db().collection("unmatched_payments").add(
            {"reference": reference, "paid_kobo": paid, "at": firestore.SERVER_TIMESTAMP})
        return jsonify(status="unmatched")  # still 200, so Paystack stops retrying
    meta = ref_doc.to_dict()
    tid = meta["tenant_id"]

    if meta["purpose"] == "wallet_topup":
        if currency != "NGN":
            return jsonify(status="ignored")
        _, applied = wallet.credit(tid, paid, "topup", reference)
        if applied:
            append_event(tid, "paystack", "wallet_topped_up", {"reference": reference, "kobo": paid})
        return jsonify(status="credited" if applied else "duplicate")

    bref = tenant_ref(tid).collection("batches").document(meta["batch_id"])
    rref = bref.collection("rows").document(meta["row_id"])
    pref = tenant_ref(tid).collection("payments").document(reference)
    result = _match(get_db().transaction(), pref, rref, bref, paid, currency, reference)
    if result in ("matched", "mismatch"):
        append_event(tid, "paystack", f"payment_{result}",
                     {"reference": reference, "paid_kobo": paid, "expected_kobo": meta["expected_kobo"]})
    if result == "matched":
        s = current_app.config["SETTINGS"]
        sender.send_receipt(tid, _adapters(), s.message_price_kobo, rref.get().to_dict(), paid, reference, pref)
    return jsonify(status=result)
