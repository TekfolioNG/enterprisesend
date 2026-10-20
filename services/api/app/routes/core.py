from flask import Blueprint, g, jsonify

from ..auth import require_auth

bp = Blueprint("core", __name__)


@bp.get("/healthz")
def healthz():
    return jsonify(status="ok")


@bp.get("/v1/me")
@require_auth()
def me():
    return jsonify(uid=g.uid, tenant_id=g.tenant_id, role=g.role)
