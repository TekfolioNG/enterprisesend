import io
import uuid
from datetime import datetime, timedelta

import pytest

from tests.emu import bearer, emulators_up, make_token

from app import create_app
from app.audit import verify_chain
from app.db import tenant_ref
from app.validation import COLUMNS, LAGOS

pytestmark = pytest.mark.skipif(not emulators_up(), reason="Firebase emulators are not running")


@pytest.fixture()
def client():
    return create_app().test_client()


@pytest.fixture()
def tenant():
    return f"tenant-{uuid.uuid4().hex[:8]}"


def csv_file(n=2):
    send = (datetime.now(LAGOS) + timedelta(days=2)).strftime("%Y-%m-%d 09:00:00")
    tag = uuid.uuid4().hex[:6]
    lines = [",".join(COLUMNS)]
    for i in range(n):
        lines.append(f'"{tag}-{i}","Ada Obi","ada{i}@example.com","2348012345678","50000",'
                     f'"2027-01-31","{send}","First Term Tuition"')
    return "\n".join(lines).encode()


def upload(client, token, data=None, **kw):
    data = data or csv_file()
    return client.post("/v1/batches", headers=bearer(token), content_type="multipart/form-data",
                       data={"file": (io.BytesIO(data), "bills.csv")}, **kw)


def test_no_token_is_rejected(client):
    assert client.get("/v1/batches").status_code == 401


def test_bad_file_rejected_and_nothing_stored(client, tenant):
    maker, _ = make_token(tenant, "maker")
    bad = csv_file().replace(b"2348012345678", b"0801", 1)
    r = upload(client, maker, bad)
    assert r.status_code == 422 and r.json["errors"][0]["column"] == "phone_whatsapp"
    assert client.get("/v1/batches", headers=bearer(maker)).json["batches"] == []


def test_upload_approve_and_audit_chain(client, tenant):
    maker, _ = make_token(tenant, "maker")
    checker, _ = make_token(tenant, "checker")
    r = upload(client, maker)
    assert r.status_code == 201
    batch_id = r.json["batch_id"]

    assert client.post(f"/v1/batches/{batch_id}/approve", headers=bearer(checker)).status_code == 200
    assert client.get(f"/v1/batches/{batch_id}", headers=bearer(maker)).json["status"] == "approved"

    entries = [d.to_dict() for d in tenant_ref(tenant).collection("audit").order_by("seq").stream()]
    assert [e["action"] for e in entries] == ["batch_uploaded", "batch_approved"]
    assert verify_chain(entries)


def test_maker_cannot_approve(client, tenant):
    maker, _ = make_token(tenant, "maker")
    batch_id = upload(client, maker).json["batch_id"]
    assert client.post(f"/v1/batches/{batch_id}/approve", headers=bearer(maker)).status_code == 403


def test_uploader_cannot_approve_own_batch(client, tenant):
    admin, _ = make_token(tenant, "admin")
    batch_id = upload(client, admin).json["batch_id"]
    r = client.post(f"/v1/batches/{batch_id}/approve", headers=bearer(admin))
    assert r.status_code == 403
    actions = [d.to_dict()["action"] for d in tenant_ref(tenant).collection("audit").stream()]
    assert "self_approval_blocked" in actions


def test_same_file_twice_is_refused(client, tenant):
    maker, _ = make_token(tenant, "maker")
    data = csv_file()
    first = upload(client, maker, data)
    second = upload(client, maker, data)
    assert second.status_code == 409 and second.json["existing_batch"] == first.json["batch_id"]


def test_clients_cannot_see_each_others_data(client):
    a, b = f"tenant-a-{uuid.uuid4().hex[:6]}", f"tenant-b-{uuid.uuid4().hex[:6]}"
    maker_a, _ = make_token(a, "maker")
    maker_b, _ = make_token(b, "maker")
    checker_b, _ = make_token(b, "checker")
    batch_id = upload(client, maker_a).json["batch_id"]

    assert client.get(f"/v1/batches/{batch_id}", headers=bearer(maker_b)).status_code == 404
    assert client.get("/v1/batches", headers=bearer(maker_b)).json["batches"] == []
    assert client.post(f"/v1/batches/{batch_id}/approve", headers=bearer(checker_b)).status_code == 404
    # and tenant A's batch is still untouched
    assert client.get(f"/v1/batches/{batch_id}", headers=bearer(maker_a)).json["status"] == "checked"
