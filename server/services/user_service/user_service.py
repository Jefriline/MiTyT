from flask import session

from dtos.user_dto.user_upload_dto import UserUploadResponseDTO
from repositories.user_repository.user_repository import UserRepository
from utils.excel_aprendiz.parser import parse_excel_to_aprendices


class UserService:
    def __init__(self) -> None:
        self.repository = UserRepository()

    def upload_excel(self, file_stream: bytes, filename: str) -> UserUploadResponseDTO:
        rows_to_upsert, errors, warnings = parse_excel_to_aprendices(file_stream)

        if not rows_to_upsert:
            return UserUploadResponseDTO(
                inserted_count=0,
                updated_count=0,
                total_rows=0,
                errors=errors if errors else ["No hay filas validas para insertar"],
                warnings=warnings,
            )

        total_processed, _ = self.repository.upsert_many(rows_to_upsert)
        return UserUploadResponseDTO(
            inserted_count=total_processed,
            updated_count=0,
            total_rows=len(rows_to_upsert),
            errors=errors,
            warnings=warnings,
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
                return {"error": "Usuario no encontrado", "user": None}
            return {"user": user, "error": None}
        except Exception as e:
            print(f"Service Error: {e}")
            return {"error": "Internal service error", "user": None}