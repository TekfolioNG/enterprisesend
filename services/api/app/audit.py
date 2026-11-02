"""Append-only, hash-chained audit log. Editing any past entry breaks every later hash."""
import hashlib
import json
from datetime import datetime, timezone

from google.cloud import firestore

from .db import get_db, tenant_ref

GENESIS = "0" * 64


def entry_hash(prev_hash: str, payload: dict) -> str:
    body = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256((prev_hash + body).encode("utf-8")).hexdigest()


def find_break(entries: list):
    """Returns the seq of the first entry that does not fit the chain, or None if intact."""
    prev = GENESIS
    for i, e in enumerate(entries, start=1):
        payload = {k: e[k] for k in ("seq", "actor", "action", "detail", "at")}
        if e["seq"] != i or e["prev_hash"] != prev or entry_hash(prev, payload) != e["hash"]:
            return e["seq"]
        prev = e["hash"]
    return None


def verify_chain(entries: list) -> bool:
    return find_break(entries) is None


@firestore.transactional
def _append(txn, head_ref, col, actor, action, detail):
    head = head_ref.get(transaction=txn)
    prev = head.get("last_hash") if head.exists else GENESIS
    seq = (head.get("seq") if head.exists else 0) + 1
    payload = {"seq": seq, "actor": actor, "action": action, "detail": detail or {},
               "at": datetime.now(timezone.utc).isoformat()}
    h = entry_hash(prev, payload)
    txn.set(col.document(f"{seq:012d}"), {**payload, "prev_hash": prev, "hash": h})
    txn.set(head_ref, {"last_hash": h, "seq": seq})
    return h


def append_event(tenant_id: str, actor: str, action: str, detail: dict | None = None) -> str:
    t = tenant_ref(tenant_id)
    return _append(get_db().transaction(), t.collection("meta").document("audit_head"),
                   t.collection("audit"), actor, action, detail)
