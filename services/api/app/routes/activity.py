from flask import Blueprint, g, jsonify, request
from google.cloud import firestore

from ..audit import find_break
from ..auth import require_auth
from ..db import tenant_ref
from ..sender import bill_message

bp = Blueprint("activity", __name__)


def _mask_phone(p: str) -> str:
    return p[:3] + "*" * max(len(p) - 6, 0) + p[-3:] if p else ""


def _mask_email(e: str) -> str:
    name, _, domain = e.partition("@")
    return (name[:1] + "***@" + domain) if domain else ""


@bp.get("/v1/audit")
@require_auth("checker", "admin")
def list_audit():
    limit = min(int(request.args.get("limit", 100)), 500)
    q = tenant_ref(g.tenant_id).collection("audit").order_by(
        "seq", direction=firestore.Query.DESCENDING).limit(limit)
    return jsonify(entries=[d.to_dict() for d in q.stream()])


@bp.get("/v1/audit/verify")
@require_auth("checker", "admin")
def verify_audit():
    t = tenant_ref(g.tenant_id)
    entries = [d.to_dict() for d in t.collection("audit").order_by("seq").stream()]
    broken = find_break(entries)
    head = t.collection("meta").document("audit_head").get()
    if entries:
        head_ok = head.exists and head.get("seq") == entries[-1]["seq"] \
            and head.get("last_hash") == entries[-1]["hash"]
    else:
        head_ok = not head.exists
    return jsonify(intact=broken is None and head_ok, entries=len(entries),
                   broken_at_seq=broken, head_matches=head_ok,
                   last_hash=entries[-1]["hash"] if entries else None)


@bp.get("/v1/batches/<batch_id>/messages")
@require_auth()
def batch_messages(batch_id):
    t = tenant_ref(g.tenant_id)
    bref = t.collection("batches").document(batch_id)
    if not bref.get().exists:
        return jsonify(error="Batch not found"), 404
    out = []
    for d in bref.collection("rows").order_by("row").limit(500).stream():
        r = d.to_dict()
        receipt = []
        if r.get("payment_ref") and r.get("status") in ("paid", "paid_mismatch"):
            p = t.collection("payments").document(r["payment_ref"]).get()
            if p.exists:
                receipt = p.to_dict().get("receipt_attempts", [])
        out.append({
            "row": r["row"], "account_id": r["account_id"], "recipient_name": r["recipient_name"],
            "phone": _mask_phone(r["phone"]), "email": _mask_email(r["primary_email"]),
            "amount_kobo": r["amount_kobo"], "status": r["status"], "paid_kobo": r.get("paid_kobo"),
            "attempts": r.get("attempts", []), "receipt_attempts": receipt,
            "payment_url": r.get("payment_url"),
            "preview": bill_message(r, r["payment_url"]) if r.get("payment_url") else None})
    return jsonify(messages=out)
