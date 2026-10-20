"""Identity Platform token check. The tenant ID comes ONLY from the verified token."""
from functools import wraps

import firebase_admin
from firebase_admin import auth as fb_auth
from flask import current_app, g, jsonify, request


def _init():
    if not firebase_admin._apps:
        firebase_admin.initialize_app()


def require_auth(*roles):
    def deco(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            header = request.headers.get("Authorization", "")
            if not header.startswith("Bearer "):
                return jsonify(error="Missing token"), 401
            _init()
            try:
                claims = fb_auth.verify_id_token(header[7:], check_revoked=True)
            except Exception:
                return jsonify(error="Invalid or expired token"), 401
            settings = current_app.config["SETTINGS"]
            mfa = claims.get("firebase", {}).get("sign_in_second_factor")
            if settings.require_mfa and not mfa:
                return jsonify(error="MFA required"), 403
            tenant_id, role = claims.get("tenant_id"), claims.get("role")
            if not tenant_id or not role:
                return jsonify(error="Account not assigned to a client"), 403
            if roles and role not in roles:
                return jsonify(error="Insufficient role"), 403
            g.uid, g.tenant_id, g.role = claims["uid"], tenant_id, role
            return fn(*args, **kwargs)
        return wrapper
    return deco
