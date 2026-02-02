from copy import deepcopy

from config.firebase.config_firebase import db
from utils.excel_aprendiz.constants import BATCH_SIZE_UPLOAD
from utils.excel_aprendiz.normalize import normalize_document_key


class UserRepository:
    def upsert_many(self, rows: list[dict]) -> tuple[int, int]:
        total_processed = 0
        batch: dict[str, dict] = {}
        for row in rows:
            firebase_key = row.pop("_firebase_key", None)
            if not firebase_key:
                continue
            user_data = deepcopy(row)
            path = f"users/{firebase_key}"
            batch[path] = user_data
            total_processed += 1
            if len(batch) >= BATCH_SIZE_UPLOAD:
                db.update(batch)
                batch = {}
        if batch:
            db.update(batch)
        return total_processed, 0

    def find_by_document(self, doc_number: str) -> dict | None:
        doc_key = normalize_document_key(doc_number) if doc_number else None
        if not doc_key:
            return None
        snapshot = db.child("users").child(doc_key).get()
        if snapshot is None:
            return None
        user_data = snapshot.val() if hasattr(snapshot, "val") else snapshot
        if not isinstance(user_data, dict):
            return None
        return user_data

    def get_admin_password_hash(self, email_key: str) -> str | None:
        if not email_key:
            return None

        snapshot = db.child("admins").child(email_key).get()
        if snapshot is None:
            return None

        admin_data = snapshot.val() if hasattr(snapshot, "val") else snapshot
        if not isinstance(admin_data, dict):
            return None

        stored_password_hash = admin_data.get("password")
        if not isinstance(stored_password_hash, str):
            return None

        return stored_password_hash