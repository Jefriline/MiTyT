import time

from config.firebase.config_firebase import db

BATCH_SIZE = 20
DELAY_SECONDS = 0.05


class UserRepository:
    def __init__(self):
        self._users = [
            {
                "Nombre": "Juan Perez",
                "TipoDocumento": "CC",
                "Nro_Documento": "10102020",
                "correo": "juan.perez@soy.sena.edu.co",
                "InformacionFormacion": {
                    "Regional": "Quindío",
                    "CentroFormacion": "Centro de Comercio y Turismo",
                    "CorreoContacto": "contacto.centro@sena.edu.co",
                    "Ficha": "2502143",
                    "Programa": "ADSO",
                    "Modalidad": "Presencial",
                    "Avance": "45%"
                },
                "InformacionConvocatoria": {
                    "Convocatoria": "Convocatoria Apoyo Sostenimiento 2026",
                    "EstadoTerminos": "Accepted",
                    "EstadoConvocatoria": "In Progress",
                    "ResponsablePago": "SENA",
                    "Observaciones": "Everything in order"
                }
            }
        ]

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
    
    def find_by_document(self, doc_number: str):
        return next((user for user in self._users if user["Nro_Documento"] == doc_number), None)