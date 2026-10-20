"""Keeps every uploaded file exactly as received. Local folder in dev, Cloud Storage elsewhere."""
import os
from pathlib import Path

from werkzeug.utils import secure_filename


def save_original(tenant_id: str, batch_id: str, filename: str, data: bytes) -> str:
    path = f"{tenant_id}/{batch_id}/{secure_filename(filename) or 'upload'}"
    bucket = os.getenv("UPLOAD_BUCKET")
    if not bucket:
        target = Path(".local_storage") / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        return f"local://{path}"
    from google.cloud import storage
    storage.Client().bucket(bucket).blob(path).upload_from_string(data)
    return f"gs://{bucket}/{path}"
