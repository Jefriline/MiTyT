from flask import session
from werkzeug.security import generate_password_hash

from dtos.user_dto.admin_dto import AdminLoginDTO
from dtos.user_dto.user_upload_dto import UserUploadResponseDTO
from repositories.user_repository.user_repository import UserRepository
from utils.auth.normalize_email import normalize_email_key
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

    def login_admin(self, credentials: AdminLoginDTO) -> bool:
        email_key = normalize_email_key(credentials.email)
        if not email_key:
            print("Email de administrador invalido")
            return False

        password_hash = generate_password_hash(credentials.password)
        is_valid_admin = self.repository.authenticate_admin(
            email_key=email_key,
            password_hash=password_hash,
        )
        if not is_valid_admin:
            print("Credenciales incorrectas")
            return False

        session["login_user"] = {
            "username": credentials.email,
            "role": "admin",
        }
        return True

    def search_user(self, doc_number: str):
        try:
            user = self.repository.find_by_document(doc_number)
            if not user:
                return {"error": "Usuario no encontrado", "user": None}
            return {"user": user, "error": None}
        except Exception as e:
            print(f"Service Error: {e}")
            return {"error": "Internal service error", "user": None}