import hashlib
import hmac

from adapters.paystack import verify_signature
from app import create_app
from app.audit import GENESIS, entry_hash, verify_chain


def _chain(n=3):
    prev, out = GENESIS, []
    for i in range(1, n + 1):
        p = {"seq": i, "actor": "u1", "action": f"a{i}", "detail": {}, "at": "2026-01-01T00:00:00Z"}
        h = entry_hash(prev, p)
        out.append({**p, "prev_hash": prev, "hash": h})
        prev = h
    return out


def test_health():
    assert create_app().test_client().get("/healthz").json == {"status": "ok"}


def test_me_requires_token():
    assert create_app().test_client().get("/v1/me").status_code == 401


def test_chain_valid_then_tamper_detected():
    chain = _chain()
    assert verify_chain(chain)
    chain[1]["action"] = "edited"
    assert not verify_chain(chain)


def test_paystack_signature():
    body, secret = b'{"event":"charge.success"}', "sk_test_x"
    good = hmac.new(secret.encode(), body, hashlib.sha512).hexdigest()
    assert verify_signature(secret, body, good)
    assert not verify_signature(secret, body, "bad")
