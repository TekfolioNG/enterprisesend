import hashlib
import hmac
import os

import requests


def verify_signature(secret: str, raw_body: bytes, header_value: str) -> bool:
    """Paystack signs webhooks with HMAC-SHA512 of the raw body. Always verify first."""
    expected = hmac.new(secret.encode(), raw_body, hashlib.sha512).hexdigest()
    return hmac.compare_digest(expected, header_value or "")


def initialize_transaction(email: str, amount_naira: float, reference: str,
                           metadata: dict | None = None) -> dict:
    """Returns Paystack's data block (authorization_url, reference). Amount is sent in kobo."""
    r = requests.post("https://api.paystack.co/transaction/initialize", timeout=10,
        headers={"Authorization": f"Bearer {os.environ['PAYSTACK_SECRET_KEY']}"},
        json={"email": email, "amount": int(round(amount_naira * 100)),
              "reference": reference, "metadata": metadata or {}})
    r.raise_for_status()
    return r.json()["data"]


def mock_initialize_transaction(email: str, amount_naira: float, reference: str,
                                metadata: dict | None = None) -> dict:
    """Local development only (PAYSTACK_MOCK=true). Never used when real keys are set."""
    return {"authorization_url": f"https://paystack.local/pay/{reference}", "reference": reference}
