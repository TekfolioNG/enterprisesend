"""Creates fixed local test users for manual testing and the web app.
Run with the emulators up:  python scripts/seed_local_users.py"""
import os
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "demo-enterprisesend")
os.environ.setdefault("FIREBASE_AUTH_EMULATOR_HOST", "localhost:9099")
import requests
from firebase_admin import auth as fb_auth
from app.auth import _init

PASSWORD = "Passw0rd!test"
USERS = [("admin@client-a.test", "client-a", "admin"), ("maker@client-a.test", "client-a", "maker"), ("checker@client-a.test", "client-a", "checker"),
         ("maker@client-b.test", "client-b", "maker"), ("checker@client-b.test", "client-b", "checker")]

_init()
base = f"http://{os.environ['FIREBASE_AUTH_EMULATOR_HOST']}/identitytoolkit.googleapis.com/v1/accounts"
for email, tenant, role in USERS:
    r = requests.post(f"{base}:signUp?key=fake", json={"email": email, "password": PASSWORD}).json()
    uid = r.get("localId") or fb_auth.get_user_by_email(email).uid
    fb_auth.set_custom_user_claims(uid, {"tenant_id": tenant, "role": role})
    print(f"{role:8s} {tenant}  {email}  password: {PASSWORD}")
