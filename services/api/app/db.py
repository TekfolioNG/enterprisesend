from google.cloud import firestore

_client = None


def get_db() -> firestore.Client:
    global _client
    if _client is None:
        _client = firestore.Client()
    return _client


def tenant_ref(tenant_id: str):
    """Every record lives under tenants/{tenant_id}/... Never query across tenants."""
    if not tenant_id:
        raise ValueError("tenant_id is required")
    return get_db().collection("tenants").document(tenant_id)
