"""Sending: wallet debit -> provider send -> refund on failure. Safe to re-run."""
import hashlib
from datetime import datetime, timedelta, timezone

from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from . import wallet
from .db import get_db, tenant_ref

CHANNEL_TARGET = {"sms": "phone", "whatsapp": "phone", "email": "primary_email"}
LOCK_SECONDS = 300


def contact_hash(contact: str) -> str:
    return hashlib.sha256(contact.strip().lower().encode()).hexdigest()


def is_suppressed(tenant_id, contact) -> bool:
    return tenant_ref(tenant_id).collection("suppressions").document(contact_hash(contact)).get().exists


def naira(kobo) -> str:
    return f"₦{kobo / 100:,.2f}"


def bill_message(row, link):
    return (f"Dear {row['recipient_name']}, your bill of {naira(row['amount_kobo'])} for "
            f"{row['description'] or 'your account'} is due {row['bill_due_date']}. "
            f"Pay securely: {link}  Reply STOP to opt out.")


def receipt_message(row, paid_kobo, reference):
    return (f"Dear {row['recipient_name']}, we received your payment of {naira(paid_kobo)} for "
            f"{row['description'] or 'your account'}. Reference: {reference}. Thank you.  "
            f"Reply STOP to opt out.")


def dispatch(tenant_id, adapters, prices, key, channel, to, text, subject=""):
    """Returns (result, info): accepted | failed | unfunded."""
    price = prices[channel]
    try:
        wallet.debit(tenant_id, price, f"send:{channel}", f"debit-{key}-{channel}")
    except wallet.InsufficientFunds:
        return "unfunded", ""
    res = adapters[channel].send(to, text, subject)
    if not res.ok:
        wallet.credit(tenant_id, price, f"refund:{channel}", f"refund-{key}-{channel}")
        return "failed", res.error
    return "accepted", res.provider_ref


@firestore.transactional
def _claim(txn, bref, now):
    snap = bref.get(transaction=txn)
    if not snap.exists:
        return "not_found"
    b = snap.to_dict()
    if b["status"] not in ("approved", "sending", "needs_funding"):
        return "bad_status"
    lock = b.get("lock_until")
    if lock and lock > now:
        return "busy"
    txn.update(bref, {"status": "sending", "lock_until": now + timedelta(seconds=LOCK_SECONDS)})
    return "ok"


def _send_row(tenant_id, batch_id, bref, doc, adapters, link_fn, prices, channels):
    r = doc.to_dict()
    reference = f"es-{batch_id}-{doc.id}"
    url = r.get("payment_url")
    if not url:
        get_db().collection("payment_refs").document(reference).set({
            "tenant_id": tenant_id, "batch_id": batch_id, "row_id": doc.id,
            "expected_kobo": r["amount_kobo"], "purpose": "bill"})
        try:
            url = link_fn(r["primary_email"], r["amount_kobo"] / 100, reference,
                          {"tenant_id": tenant_id, "batch_id": batch_id})["authorization_url"]
        except Exception:
            doc.reference.update({"status": "failed", "error": "payment_link_failed"})
            bref.update({"failed_count": firestore.Increment(1)})
            return "failed"
        doc.reference.update({"payment_ref": reference, "payment_url": url})

    text = bill_message(r, url)
    attempts = list(r.get("attempts", []))
    done = {a["channel"] for a in attempts if a["result"] == "accepted"}
    unfunded = False
    for ch in channels:
        if ch in done:
            continue
        to = r[CHANNEL_TARGET[ch]]
        if is_suppressed(tenant_id, to):
            attempts.append({"channel": ch, "result": "suppressed"})
            continue
        result, info = dispatch(tenant_id, adapters, prices, f"{batch_id}-{doc.id}", ch, to, text,
                                "Your bill")
        attempts.append({"channel": ch, "result": result, "info": info,
                         "at": datetime.now(timezone.utc).isoformat()})
        if result == "unfunded":
            unfunded = True
            break
        if result == "accepted":
            done.add(ch)

    results = {a["result"] for a in attempts}
    if done:
        status = "sent"
        bref.update({"sent_count": firestore.Increment(1),
                     "sent_kobo": firestore.Increment(r["amount_kobo"])})
    elif unfunded:
        status = "unfunded"
    elif results == {"suppressed"}:
        status = "suppressed"
    else:
        status = "failed"
        bref.update({"failed_count": firestore.Increment(1)})
    doc.reference.update({"status": status, "attempts": attempts})
    return status


def process_batch(tenant_id, batch_id, adapters, link_fn, prices, channels, now=None):
    """Sends every due row of an approved batch. Future rows wait; call again later."""
    now = now or datetime.now(timezone.utc)
    bref = tenant_ref(tenant_id).collection("batches").document(batch_id)
    claim = _claim(get_db().transaction(), bref, now)
    if claim != "ok":
        return {"result": claim}
    stats = {"sent": 0, "failed": 0, "unfunded": 0, "suppressed": 0, "scheduled": 0}
    try:
        todo = bref.collection("rows").where(
            filter=FieldFilter("status", "in", ["pending", "unfunded"])).stream()
        for doc in todo:
            if datetime.fromisoformat(doc.to_dict()["send_at"]) > now:
                stats["scheduled"] += 1
                continue
            stats[_send_row(tenant_id, batch_id, bref, doc, adapters, link_fn, prices, channels)] += 1
    finally:
        def any_with(status):
            q = bref.collection("rows").where(filter=FieldFilter("status", "==", status)).limit(1)
            return any(True for _ in q.stream())
        status = "sending" if any_with("pending") else ("needs_funding" if any_with("unfunded") else "completed")
        bref.update({"status": status, "lock_until": None})
    return {"result": "ok", "status": status, **stats}


def send_receipt(tenant_id, adapters, prices, row, paid_kobo, reference, pref):
    text = receipt_message(row, paid_kobo, reference)
    attempts = []
    for ch in ("email", "whatsapp"):
        to = row[CHANNEL_TARGET[ch]]
        if is_suppressed(tenant_id, to):
            attempts.append({"channel": ch, "result": "suppressed"})
            continue
        result, info = dispatch(tenant_id, adapters, prices, f"receipt-{reference}", ch, to, text,
                                "Payment receipt")
        attempts.append({"channel": ch, "result": result, "info": info})
    pref.update({"receipt_attempts": attempts})
