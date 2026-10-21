"""Local demo helpers. Run with the emulators AND the API running.
  PYTHONPATH=. python scripts/dev_tools.py credit client-a 5000
  PYTHONPATH=. python scripts/dev_tools.py pay client-a <batch-id-prefix> [row-number=1]
Start the API with PAYSTACK_SECRET_KEY=sk_test_local PAYSTACK_MOCK=true so 'pay' signatures match."""
import hashlib
import hmac
import json
import os
import sys
import uuid

os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "demo-enterprisesend")
os.environ.setdefault("FIRESTORE_EMULATOR_HOST", "localhost:8085")

import requests  # noqa: E402

from app import wallet  # noqa: E402
from app.db import tenant_ref  # noqa: E402

SECRET = os.getenv("PAYSTACK_SECRET_KEY", "sk_test_local")
API = os.getenv("API_BASE", "http://localhost:8080")


def credit(tenant, naira):
    bal, _ = wallet.credit(tenant, int(float(naira) * 100), "dev top-up", f"dev-credit-{uuid.uuid4().hex}")
    print(f"Wallet for {tenant} is now ₦{bal / 100:,.2f}")


def pay(tenant, prefix, n=1):
    batches = [b for b in tenant_ref(tenant).collection("batches").stream() if b.id.startswith(prefix)]
    if len(batches) != 1:
        sys.exit(f"Expected one batch starting with '{prefix}', found {len(batches)}")
    rows = [r.to_dict() for r in batches[0].reference.collection("rows").order_by("row").stream()]
    row = rows[int(n) - 1]
    if not row.get("payment_ref"):
        sys.exit("That row has no payment link yet. Send the batch first.")
    body = json.dumps({"event": "charge.success", "data": {
        "reference": row["payment_ref"], "amount": row["amount_kobo"], "currency": "NGN"}}).encode()
    sig = hmac.new(SECRET.encode(), body, hashlib.sha512).hexdigest()
    r = requests.post(f"{API}/webhooks/paystack", data=body,
                      headers={"X-Paystack-Signature": sig, "Content-Type": "application/json"})
    print(r.status_code, r.text.strip())


if __name__ == "__main__":
    cmd, *args = sys.argv[1:] or ["help"]
    {"credit": credit, "pay": pay}.get(cmd, lambda *a: print(__doc__))(*args)
