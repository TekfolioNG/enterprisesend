"""Create (or reset) a user on the REAL Identity Platform with tenant and role claims.
  python scripts/create_user.py EMAIL TENANT_ID ROLE      (ROLE: maker | checker | admin)
Run with:  GOOGLE_CLOUD_PROJECT=enterprisesend-staging  and NO emulator variables set.
The password is typed hidden. Emails are marked verified, which two-step sign-in (MFA) requires."""
import getpass
import os
import sys

import firebase_admin
from firebase_admin import auth

if os.getenv("FIREBASE_AUTH_EMULATOR_HOST"):
    sys.exit("FIREBASE_AUTH_EMULATOR_HOST is set: unset it, this script is for the real project.")
project = os.getenv("GOOGLE_CLOUD_PROJECT", "enterprisesend-staging")
if len(sys.argv) != 4 or sys.argv[3] not in {"maker", "checker", "admin"}:
    sys.exit(__doc__)
email, tenant, role = sys.argv[1:]
password = getpass.getpass("Password (at least 12 characters): ")
if len(password) < 12:
    sys.exit("Password too short.")

firebase_admin.initialize_app(options={"projectId": project})
try:
    user = auth.create_user(email=email, password=password, email_verified=True)
except auth.EmailAlreadyExistsError:
    user = auth.get_user_by_email(email)
    auth.update_user(user.uid, password=password, email_verified=True)
auth.set_custom_user_claims(user.uid, {"tenant_id": tenant, "role": role})
print(f"{email}: tenant={tenant} role={role} (sign out and in again to pick up changes)")
