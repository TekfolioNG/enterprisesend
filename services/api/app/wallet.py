"""Prepaid wallet as an append-only ledger. The balance is derived in the same transaction
as each entry, and the entry ID is the idempotency key, so a repeat can never double-apply."""
from google.cloud import firestore

from .db import get_db, tenant_ref


class InsufficientFunds(Exception):
    pass


def _wallet_ref(tenant_id):
    return tenant_ref(tenant_id).collection("meta").document("wallet")


def _entry_ref(tenant_id, ref):
    return tenant_ref(tenant_id).collection("wallet_ledger").document(ref.replace("/", "_"))


@firestore.transactional
def _apply(txn, wref, eref, delta, reason, ref):
    entry = eref.get(transaction=txn)
    if entry.exists:
        return entry.get("balance_after_kobo"), False  # replay: nothing changes
    w = wref.get(transaction=txn)
    new = (w.get("balance_kobo") if w.exists else 0) + delta
    if new < 0:
        raise InsufficientFunds()
    txn.set(wref, {"balance_kobo": new})
    txn.set(eref, {"delta_kobo": delta, "reason": reason, "ref": ref,
                   "balance_after_kobo": new, "at": firestore.SERVER_TIMESTAMP})
    return new, True


def credit(tenant_id, kobo, reason, ref):
    """Returns (balance_after, applied). applied is False if this ref was already used."""
    return _apply(get_db().transaction(), _wallet_ref(tenant_id), _entry_ref(tenant_id, ref),
                  int(kobo), reason, ref)


def debit(tenant_id, kobo, reason, ref):
    return _apply(get_db().transaction(), _wallet_ref(tenant_id), _entry_ref(tenant_id, ref),
                  -int(kobo), reason, ref)


def balance(tenant_id) -> int:
    w = _wallet_ref(tenant_id).get()
    return w.get("balance_kobo") if w.exists else 0
