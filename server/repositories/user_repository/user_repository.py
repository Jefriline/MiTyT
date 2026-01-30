import time

from config.firebase.config_firebase import db

BATCH_SIZE = 20
DELAY_SECONDS = 0.05


class UserRepository:

    def insert_one(self, aprendiz: dict) -> str:
        result = db.child("users").push(aprendiz)
        return result["name"]

    def insert_many(self, rows: list[dict]) -> int:
        inserted = 0
        for index, row in enumerate(rows):
            db.child("users").push(row)
            inserted += 1
            if (index + 1) % BATCH_SIZE == 0:
                time.sleep(DELAY_SECONDS)
        return inserted
    
    def find_by_document(self, doc_number: str) -> dict | None:
        if not doc_number or not doc_number.strip():
            return None
        term = doc_number.strip()
        snapshot = (
            db.child("users")
            .order_by_child("Nro Documento")
            .equal_to(term)
            .get()
        )
        if snapshot is None or not snapshot.each():
            return None
        first = snapshot.each()[0]
        user_data = first.val()
        if not isinstance(user_data, dict):
            return None
        return user_data