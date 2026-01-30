from io import BytesIO
from flask import session
from openpyxl import load_workbook

from dtos.user_dto.user_upload_dto import UserUploadResponseDTO
from repositories.user_repository.user_repository import UserRepository

COLUMNA_NOMBRE = "nombre"
COLUMNA_EDAD = "edad"
HEADERS_ESPERADOS = (COLUMNA_NOMBRE, COLUMNA_EDAD)


class UserService:

    def __init__(self) -> None:
        self.repository = UserRepository()

    def upload_excel(self, file_stream: bytes, filename: str) -> UserUploadResponseDTO:
        
        errors: list[str] = []
        rows_to_insert: list[dict] = []

        workbook = load_workbook(filename=BytesIO(file_stream), read_only=True, data_only=True)
        sheet = workbook.active
        if not sheet:
            workbook.close()
            return UserUploadResponseDTO(
                inserted_count=0,
                total_rows=0,
                errors=["El archivo no tiene hojas o esta vacio"],
            )

        rows_iter = sheet.iter_rows(min_row=1, values_only=True)
        header_row = next(rows_iter, None)
        if not header_row:
            workbook.close()
            return UserUploadResponseDTO(
                inserted_count=0,
                total_rows=0,
                errors=["El archivo no tiene filas"],
            )

        header_normalized = [str(cell).strip().lower() if cell else "" for cell in header_row]
        if COLUMNA_NOMBRE not in header_normalized or COLUMNA_EDAD not in header_normalized:
            workbook.close()
            return UserUploadResponseDTO(
                inserted_count=0,
                total_rows=0,
                errors=["El Excel debe tener columnas 'nombre' y 'edad' en la primera fila"],
            )

        idx_nombre = header_normalized.index(COLUMNA_NOMBRE)
        idx_edad = header_normalized.index(COLUMNA_EDAD)

        for row_index, row in enumerate(rows_iter, start=2):
            if row is None:
                continue
            nombre_raw = row[idx_nombre] if idx_nombre < len(row) else None
            edad_raw = row[idx_edad] if idx_edad < len(row) else None

            nombre = str(nombre_raw).strip() if nombre_raw is not None else ""
            if not nombre:
                errors.append(f"Fila {row_index}: nombre vacio")
                continue

            try:
                edad = int(edad_raw) if edad_raw is not None else 0
            except (TypeError, ValueError):
                errors.append(f"Fila {row_index}: edad no numerica")
                continue

            if edad < 0 or edad > 150:
                errors.append(f"Fila {row_index}: edad fuera de rango (0-150)")
                continue

            rows_to_insert.append({"nombre": nombre, "edad": edad})

        workbook.close()

        if not rows_to_insert:
            return UserUploadResponseDTO(
                inserted_count=0,
                total_rows=0,
                errors=errors if errors else ["No hay filas validas para insertar"],
            )

        inserted_count = self.repository.insert_many(rows_to_insert)
        return UserUploadResponseDTO(
            inserted_count=inserted_count,
            total_rows=len(rows_to_insert),
            errors=errors,
        )

    def login_user(self, username: str, password: str) -> bool:
        if username == "admin@mityt.com" and password == "admin123":
            session['login_user'] = {
                "username": username,
                "role": "admin"
            }
            return True
        
        print("Credenciales incorrectas")
        return False

    def search_user(self, doc_number: str):
        try:
            user = self.repository.find_by_document(doc_number)
            if not user:
                return {"error": "User not found", "user": None}
            return {"user": user, "error": None}
        except Exception as e:
            print(f"Service Error: {e}")
            return {"error": "Internal service error", "user": None}