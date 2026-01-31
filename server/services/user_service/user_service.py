from io import BytesIO
from flask import session
from openpyxl import load_workbook

from dtos.user_dto.user_upload_dto import UserUploadResponseDTO
from repositories.user_repository.user_repository import UserRepository
from utils.excel_aprendiz.parser import parse_excel_to_aprendices


class UserService:

    def __init__(self) -> None:
        self.repository = UserRepository()

    def upload_excel(self, file_stream: bytes, filename: str) -> UserUploadResponseDTO:
        rows_to_insert, errors = parse_excel_to_aprendices(file_stream)

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
                return {"error": "Usuario no encontrado", "user": None}
            return {"user": user, "error": None}
        except Exception as e:
            print(f"Service Error: {e}")
            return {"error": "Internal service error", "user": None}