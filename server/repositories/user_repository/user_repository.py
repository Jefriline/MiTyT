import time

from config.firebase.config_firebase import db

BATCH_SIZE = 20
DELAY_SECONDS = 0.05


class UserRepository:
    
    def insert_one(self, nombre: str, edad: int) -> str:
        payload = {"nombre": nombre, "edad": edad}
        result = db.child("users").push(payload)
        return result["name"]

    def insert_many(self, rows: list[dict]) -> int:
        inserted = 0
        for index, row in enumerate(rows):
            nombre = row.get("nombre", "")
            edad = row.get("edad", 0)
            db.child("users").push({"nombre": nombre, "edad": edad})
            inserted += 1
            if (index + 1) % BATCH_SIZE == 0:
                time.sleep(DELAY_SECONDS)
        return inserted
