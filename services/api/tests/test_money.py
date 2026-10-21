import hashlib
import hmac
import io
import json
import uuid
from datetime import datetime, timedelta

import pytest

from tests.emu import bearer, emulators_up, make_token

from adapters.base import Adapter, SendResult
from app import create_app, wallet
from app.config import DEFAULT_PRICES
from app.db import tenant_ref
from app.validation import COLUMNS, LAGOS

pytestmark = pytest.mark.skipif(not emulators_up(), reason="Firebase emulators are not running")
SECRET = "sk_test_money"
PRICES = DEFAULT_PRICES
ALL3 = PRICES["sms"] + PRICES["whatsapp"] + PRICES["email"]
AMOUNT_KOBO = 5_000_000  # ₦50,000 in the test file


class Fake(Adapter):
    name = "fake"

    def __init__(self, channel, ok=True):
        self.channel, self.ok, self.sent = channel, ok, []

    def send(self, to, message, subject=""):
        self.sent.append((to, message))
        return SendResult(self.ok, f"r{len(self.sent)}" if self.ok else "", "" if self.ok else "boom")


@pytest.fixture()
def fakes():
    return {c: Fake(c) for c in ("sms", "whatsapp", "email")}


@pytest.fixture()
def client(fakes, monkeypatch):
    monkeypatch.setenv("PAYSTACK_SECRET_KEY", SECRET)
    app = create_app()
    app.config["ADAPTERS"] = fakes
    app.config["PAYMENT_LINK_FN"] = lambda email, amt, ref, meta=None: {"authorization_url": f"https://pay.test/{ref}"}
    return app.test_client()


@pytest.fixture()
def tenant():
    return f"tenant-{uuid.uuid4().hex[:8]}"


def csv_file(n=2, later=False):
    when = datetime.now(LAGOS) + (timedelta(days=2) if later else timedelta(0))
    tag = uuid.uuid4().hex[:6]
    lines = [",".join(COLUMNS)] + [
        f'"{tag}-{i}","Ada Obi","ada{i}@example.com","2348012345678","50000","2027-01-31",'
        f'"{when:%Y-%m-%d %H:%M:%S}","Tuition"' for i in range(n)]
    return "\n".join(lines).encode()


def approved_batch(client, tenant, n=2, later=False):
    maker, _ = make_token(tenant, "maker")
    checker, _ = make_token(tenant, "checker")
    r = client.post("/v1/batches", headers=bearer(maker), content_type="multipart/form-data",
                    data={"file": (io.BytesIO(csv_file(n, later)), "b.csv")})
    batch_id = r.json["batch_id"]
    assert client.post(f"/v1/batches/{batch_id}/approve", headers=bearer(checker)).status_code == 200
    return batch_id, maker, checker


def rows(tenant, batch_id):
    col = tenant_ref(tenant).collection("batches").document(batch_id).collection("rows")
    return [d.to_dict() for d in col.order_by("row").stream()]


def webhook(client, reference, kobo, currency="NGN", secret=SECRET):
    body = json.dumps({"event": "charge.success",
                       "data": {"reference": reference, "amount": kobo, "currency": currency}}).encode()
    sig = hmac.new(secret.encode(), body, hashlib.sha512).hexdigest()
    return client.post("/webhooks/paystack", data=body, content_type="application/json",
                       headers={"X-Paystack-Signature": sig})


def test_wallet_is_idempotent_and_never_negative(tenant):
    assert wallet.credit(tenant, 1000, "topup", "r1") == (1000, True)
    assert wallet.credit(tenant, 1000, "topup", "r1") == (1000, False)  # replay changes nothing
    wallet.debit(tenant, 400, "send", "d1")
    with pytest.raises(wallet.InsufficientFunds):
        wallet.debit(tenant, 700, "send", "d2")
    assert wallet.balance(tenant) == 600


def test_send_pay_receipt_and_replay(client, fakes, tenant):
    batch_id, maker, checker = approved_batch(client, tenant)
    wallet.credit(tenant, 1_000_000, "topup", "seed")
    out = client.post(f"/v1/batches/{batch_id}/send", headers=bearer(checker)).json
    assert out["sent"] == 2 and out["status"] == "completed"
    assert all(len(f.sent) == 2 for f in fakes.values())
    assert wallet.balance(tenant) == 1_000_000 - 2 * ALL3
    r0 = rows(tenant, batch_id)[0]
    assert r0["payment_url"] in fakes["sms"].sent[0][1]            # link is in the message

    assert webhook(client, r0["payment_ref"], AMOUNT_KOBO).json["status"] == "matched"
    assert len(fakes["email"].sent) == 3                            # 2 bills + 1 receipt
    assert webhook(client, r0["payment_ref"], AMOUNT_KOBO).json["status"] == "duplicate"
    assert len(fakes["email"].sent) == 3                            # no second receipt
    dash = client.get("/v1/dashboard", headers=bearer(maker)).json
    assert (dash["sent_count"], dash["paid_count"], dash["outstanding_kobo"]) == (2, 1, AMOUNT_KOBO)
    assert rows(tenant, batch_id)[0]["status"] == "paid"


def test_wrong_amount_is_flagged_not_matched(client, fakes, tenant):
    batch_id, maker, checker = approved_batch(client, tenant, n=1)
    wallet.credit(tenant, 1_000_000, "topup", "seed")
    client.post(f"/v1/batches/{batch_id}/send", headers=bearer(checker))
    ref = rows(tenant, batch_id)[0]["payment_ref"]
    assert webhook(client, ref, AMOUNT_KOBO - 100).json["status"] == "mismatch"
    assert rows(tenant, batch_id)[0]["status"] == "paid_mismatch"
    assert len(fakes["email"].sent) == 1                            # no receipt
    assert client.get("/v1/dashboard", headers=bearer(maker)).json["paid_count"] == 0


def test_bad_signature_is_rejected(client, tenant):
    batch_id, maker, checker = approved_batch(client, tenant, n=1)
    wallet.credit(tenant, 1_000_000, "topup", "seed")
    client.post(f"/v1/batches/{batch_id}/send", headers=bearer(checker))
    ref = rows(tenant, batch_id)[0]["payment_ref"]
    assert webhook(client, ref, AMOUNT_KOBO, secret="wrong").status_code == 401
    assert rows(tenant, batch_id)[0]["status"] == "sent"


def test_empty_wallet_stops_sending_then_resumes_without_double_send(client, fakes, tenant):
    batch_id, maker, checker = approved_batch(client, tenant)
    out = client.post(f"/v1/batches/{batch_id}/send", headers=bearer(checker)).json
    assert out["unfunded"] == 2 and out["status"] == "needs_funding"
    assert fakes["sms"].sent == []
    wallet.credit(tenant, 1_000_000, "topup", "seed")
    out = client.post(f"/v1/batches/{batch_id}/send", headers=bearer(checker)).json
    assert out["sent"] == 2 and out["status"] == "completed"
    assert len(fakes["sms"].sent) == 2                              # each customer got one SMS


def test_future_rows_wait(client, fakes, tenant):
    batch_id, maker, checker = approved_batch(client, tenant, later=True)
    wallet.credit(tenant, 1_000_000, "topup", "seed")
    out = client.post(f"/v1/batches/{batch_id}/send", headers=bearer(checker)).json
    assert out["scheduled"] == 2 and out["status"] == "sending"
    batch = tenant_ref(tenant).collection("batches").document(batch_id).get().to_dict()
    assert batch["next_send_at"] is not None
    assert all(f.sent == [] for f in fakes.values())


def test_opt_out_is_respected(client, fakes, tenant):
    batch_id, maker, checker = approved_batch(client, tenant, n=1)
    wallet.credit(tenant, 1_000_000, "topup", "seed")
    client.post("/v1/suppressions", headers=bearer(maker), json={"contact": "+2348012345678"})
    client.post(f"/v1/batches/{batch_id}/send", headers=bearer(checker))
    assert fakes["sms"].sent == [] and fakes["whatsapp"].sent == []
    assert len(fakes["email"].sent) == 1


def test_failed_send_is_refunded(client, fakes, tenant):
    fakes["sms"].ok = False
    batch_id, maker, checker = approved_batch(client, tenant, n=1)
    wallet.credit(tenant, 1_000_000, "topup", "seed")
    client.post(f"/v1/batches/{batch_id}/send", headers=bearer(checker))
    assert wallet.balance(tenant) == 1_000_000 - PRICES["whatsapp"] - PRICES["email"]


def test_other_client_cannot_send_this_batch(client, tenant):
    batch_id, maker, checker = approved_batch(client, tenant, n=1)
    other, _ = make_token(f"tenant-{uuid.uuid4().hex[:8]}", "checker")
    assert client.post(f"/v1/batches/{batch_id}/send", headers=bearer(other)).status_code == 404
    assert client.post(f"/v1/batches/{batch_id}/send", headers=bearer(maker)).status_code == 403


def test_topup_through_webhook(client, tenant):
    admin, _ = make_token(tenant, "admin")
    r = client.post("/v1/wallet/topup", headers=bearer(admin), json={"amount_naira": 5000}).json
    assert webhook(client, r["reference"], 500_000).json["status"] == "credited"
    assert webhook(client, r["reference"], 500_000).json["status"] == "duplicate"
    assert wallet.balance(tenant) == 500_000
