"""Helpers for tests that run against the local Firebase emulators.
Run the emulators first: services/api/scripts/run_emulators.sh"""
import os
import socket
import uuid

os.environ.setdefault("ENVIRONMENT", "local")
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "demo-enterprisesend")
os.environ.setdefault("FIRESTORE_EMULATOR_HOST", "localhost:8085")
os.environ.setdefault("FIREBASE_AUTH_EMULATOR_HOST", "localhost:9099")

import requests  # noqa: E402
from firebase_admin import auth as fb_auth  # noqa: E402

from app.auth import _init  # noqa: E402

AUTH = os.environ["FIREBASE_AUTH_EMULATOR_HOST"]
FIRESTORE = os.environ["FIRESTORE_EMULATOR_HOST"]
PASSWORD = "Passw0rd!test"


def _port_open(hostport: str) -> bool:
    host, port = hostport.split(":")
    try:
        with socket.create_connection((host, int(port)), timeout=0.5):
            return True
    except OSError:
        return False


def emulators_up() -> bool:
    return _port_open(AUTH) and _port_open(FIRESTORE)


def make_token(tenant_id: str, role: str, email: str | None = None) -> tuple[str, str]:
    """Creates an emulator user with tenant and role claims. Returns (id_token, uid)."""
    _init()
    email = email or f"{role}-{uuid.uuid4().hex[:8]}@test.local"
    base = f"http://{AUTH}/identitytoolkit.googleapis.com/v1/accounts"
    uid = requests.post(f"{base}:signUp?key=fake", json={
        "email": email, "password": PASSWORD, "returnSecureToken": True}).json()["localId"]
    fb_auth.set_custom_user_claims(uid, {"tenant_id": tenant_id, "role": role})
    token = requests.post(f"{base}:signInWithPassword?key=fake", json={
        "email": email, "password": PASSWORD, "returnSecureToken": True}).json()["idToken"]
    return token, uid


def bearer(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}
