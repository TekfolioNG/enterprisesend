import hashlib
import uuid

from flask import Blueprint, Response, current_app, g, jsonify, request
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from ai.gateway import flag_anomalies

from ..audit import append_event
from ..auth import require_auth
from ..db import get_db, tenant_ref
from ..storage import save_original
from ..validation import build_template_xlsx, parse_file, validate_rows

bp = Blueprint("batches", __name__)


def _batches():
    return tenant_ref(g.tenant_id).collection("batches")


def _public(doc):
    d = doc.to_dict()
    for k in ("created_at", "approved_at"):
        if d.get(k):
            d[k] = d[k].isoformat()
    return {"id": doc.id, **d}


@bp.get("/v1/template.xlsx")
@require_auth()
def template():
    return Response(build_template_xlsx(), headers={
        "Content-Disposition": "attachment; filename=enterprisesend-template.xlsx"},
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@bp.post("/v1/batches")
@require_auth("maker", "admin")
def create_batch():
    file = request.files.get("file")
    if not file or not file.filename:
        return jsonify(error="Choose a file to upload"), 400
    data = file.read()
    try:
        rows = parse_file(file.filename, data)
    except ValueError as exc:
        return jsonify(error=str(exc)), 422
    clean, errors = validate_rows(rows)
    if errors:  # rejected before storage or AI
        return jsonify(error="Fix these problems and upload again",
                       error_count=len(errors), errors=errors[:200]), 422

    content_hash = hashlib.sha256(data).hexdigest()
    if not request.args.get("allow_duplicate"):
        dup = list(_batches().where(filter=FieldFilter("content_hash", "==", content_hash)).limit(1).stream())
        if dup:
            return jsonify(error="This exact file was already uploaded",
                           existing_batch=dup[0].id), 409

    batch_id = uuid.uuid4().hex
    file_uri = save_original(g.tenant_id, batch_id, file.filename, data)
    try:
        ai = flag_anomalies(current_app.config["SETTINGS"], [
            {"account_id": c["account_id"], "invoice_amount": c["amount_kobo"] / 100,
             "description": c["description"]} for c in clean])
    except Exception:
        ai = {"enabled": False, "flags": [], "error": "ai_unavailable"}

    ref = _batches().document(batch_id)
    ref.set({"status": "checked", "uploaded_by": g.uid, "file_uri": file_uri,
             "content_hash": content_hash, "row_count": len(clean),
             "total_kobo": sum(c["amount_kobo"] for c in clean), "ai": ai,
             "created_at": firestore.SERVER_TIMESTAMP})
    for i in range(0, len(clean), 400):
        wb = get_db().batch()
        for c in clean[i:i + 400]:
            wb.set(ref.collection("rows").document(f"{c['row']:06d}"), c)
        wb.commit()
    append_event(g.tenant_id, g.uid, "batch_uploaded",
                 {"batch_id": batch_id, "rows": len(clean), "sha256": content_hash})
    return jsonify(batch_id=batch_id, status="checked", rows=len(clean),
                   ai_flags=ai.get("flags", []), ai_enabled=ai.get("enabled", False)), 201


@firestore.transactional
def _approve(txn, ref, uid):
    snap = ref.get(transaction=txn)
    if not snap.exists:
        return "not_found"
    batch = snap.to_dict()
    if batch["status"] != "checked":
        return "bad_status"
    if batch["uploaded_by"] == uid:
        return "self_approval"
    txn.update(ref, {"status": "approved", "approved_by": uid,
                     "approved_at": firestore.SERVER_TIMESTAMP})
    return "ok"


@bp.post("/v1/batches/<batch_id>/approve")
@require_auth("checker", "admin")
def approve(batch_id):
    ref = _batches().document(batch_id)
    result = _approve(get_db().transaction(), ref, g.uid)
    if result == "ok":
        append_event(g.tenant_id, g.uid, "batch_approved", {"batch_id": batch_id})
        return jsonify(batch_id=batch_id, status="approved")
    if result == "self_approval":
        append_event(g.tenant_id, g.uid, "self_approval_blocked", {"batch_id": batch_id})
        return jsonify(error="The person who uploaded a batch cannot approve it"), 403
    if result == "bad_status":
        return jsonify(error="Only a checked batch can be approved"), 409
    return jsonify(error="Batch not found"), 404


@bp.get("/v1/batches/<batch_id>")
@require_auth()
def get_batch(batch_id):
    doc = _batches().document(batch_id).get()
    if not doc.exists:
        return jsonify(error="Batch not found"), 404
    return jsonify(_public(doc))


@bp.get("/v1/batches")
@require_auth()
def list_batches():
    docs = _batches().order_by("created_at", direction=firestore.Query.DESCENDING).limit(50).stream()
    return jsonify(batches=[_public(d) for d in docs])
