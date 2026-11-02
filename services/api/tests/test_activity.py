import pytest

from tests.emu import bearer, emulators_up
from tests.test_money import approved_batch, client, fakes, rows, tenant, webhook  # noqa: F401

from app import wallet
from app.db import tenant_ref

pytestmark = pytest.mark.skipif(not emulators_up(), reason="Firebase emulators are not running")


def _run_loop(client, tenant):
    batch_id, maker, checker = approved_batch(client, tenant, n=2)
    wallet.credit(tenant, 1_000_000, "topup", "seed")
    client.post(f"/v1/batches/{batch_id}/send", headers=bearer(checker))
    return batch_id, maker, checker


def test_activity_lists_events_and_chain_verifies(client, tenant):
    batch_id, maker, checker = _run_loop(client, tenant)
    actions = [e["action"] for e in client.get("/v1/audit", headers=bearer(checker)).json["entries"]]
    assert {"batch_uploaded", "batch_approved", "batch_send_run"} <= set(actions)
    v = client.get("/v1/audit/verify", headers=bearer(checker)).json
    assert v["intact"] is True and v["entries"] >= 3 and v["broken_at_seq"] is None


def test_edited_entry_is_detected(client, tenant):
    _, maker, checker = _run_loop(client, tenant)
    tenant_ref(tenant).collection("audit").document(f"{2:012d}").update({"action": "edited"})
    v = client.get("/v1/audit/verify", headers=bearer(checker)).json
    assert v["intact"] is False and v["broken_at_seq"] == 2


def test_deleted_last_entry_is_detected(client, tenant):
    _, maker, checker = _run_loop(client, tenant)
    last = client.get("/v1/audit/verify", headers=bearer(checker)).json["entries"]
    tenant_ref(tenant).collection("audit").document(f"{last:012d}").delete()
    v = client.get("/v1/audit/verify", headers=bearer(checker)).json
    assert v["intact"] is False and v["head_matches"] is False


def test_maker_cannot_read_audit(client, tenant):
    _, maker, checker = _run_loop(client, tenant)
    assert client.get("/v1/audit", headers=bearer(maker)).status_code == 403


def test_messages_show_channels_link_and_receipt(client, fakes, tenant):
    batch_id, maker, checker = _run_loop(client, tenant)
    msgs = client.get(f"/v1/batches/{batch_id}/messages", headers=bearer(maker)).json["messages"]
    assert len(msgs) == 2
    assert {a["channel"] for a in msgs[0]["attempts"]} == {"sms", "whatsapp", "email"}
    assert msgs[0]["payment_url"] in msgs[0]["preview"]
    assert "*" in msgs[0]["phone"] and "@" in msgs[0]["email"]

    ref = rows(tenant, batch_id)[0]["payment_ref"]
    webhook(client, ref, 5_000_000)
    paid = client.get(f"/v1/batches/{batch_id}/messages", headers=bearer(maker)).json["messages"][0]
    assert paid["status"] == "paid" and len(paid["receipt_attempts"]) == 2


def test_other_client_cannot_read_messages(client, tenant):
    from tests.emu import make_token
    batch_id, _, _ = _run_loop(client, tenant)
    other, _ = make_token("tenant-other-" + tenant[-6:], "maker")
    assert client.get(f"/v1/batches/{batch_id}/messages", headers=bearer(other)).status_code == 404
