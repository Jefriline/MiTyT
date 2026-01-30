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
