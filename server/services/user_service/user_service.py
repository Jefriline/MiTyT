import secrets

from flask import session
from werkzeug.security import check_password_hash

from dtos.user_dto.admin_dto import AdminLoginDTO
from dtos.user_dto.credentials_code_dto import (
    SendCodeResponseDTO,
    ValidateCodeResponseDTO,
)
from dtos.user_dto.user_upload_dto import UserUploadResponseDTO
from repositories.user_repository.user_repository import UserRepository
from utils.auth.normalize_email import normalize_email_key
from utils.excel_aprendiz.normalize import normalize_document_key
from utils.excel_aprendiz.parser import parse_excel_to_aprendices
from utils.worker.email_queue import push_email_credentials_task

CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
CODE_LENGTH = 6


def _generate_credentials_code() -> str:
    return "".join(secrets.choice(CODE_ALPHABET) for _ in range(CODE_LENGTH))


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
                errors=errors if errors else ["No hay filas válidas para insertar"],
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
            print("Email de administrador inválido")
            return False

        stored_password_hash = self.repository.get_admin_password_hash(email_key)
        if not stored_password_hash:
            print("Credenciales incorrectas")
            return False

        if not check_password_hash(stored_password_hash, credentials.password):
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

    def send_credentials_code(self, document: str) -> SendCodeResponseDTO:
        doc_key = normalize_document_key(document)
        if not doc_key:
            return SendCodeResponseDTO(success=False, message="Documento inválido.")

        user = self.repository.find_by_document(document)
        if not user or not isinstance(user, dict):
            return SendCodeResponseDTO(success=False, message="Usuario no encontrado.")

        email = (user.get("CorreoPersonal") or user.get("Correo") or "").strip()
        if not email or "@" not in email:
            return SendCodeResponseDTO(
                success=False,
                message="El usuario no tiene correo registrado.",
            )

        code = _generate_credentials_code()
        self.repository.set_user_code(doc_key, code)
        push_email_credentials_task(to_address=email, doc_key=doc_key, code=code)

        return SendCodeResponseDTO(
            success=True,
            message="Se ha enviado un código de seguridad al correo registrado.",
        )

    def validate_credentials_code(
        self, document: str, code: str
    ) -> ValidateCodeResponseDTO:
        doc_key = normalize_document_key(document)
        if not doc_key:
            return ValidateCodeResponseDTO(
                success=False,
                message="Documento inválido.",
            )

        stored_code = self.repository.get_user_code(doc_key)
        if not stored_code:
            return ValidateCodeResponseDTO(
                success=False,
                message="Código expirado o no solicitado.",
            )

        if (code or "").strip().upper() != stored_code.upper():
            return ValidateCodeResponseDTO(
                success=False,
                message="Código incorrecto.",
            )

        user = self.repository.find_by_document(document)
        if not user or not isinstance(user, dict):
            self.repository.delete_user_code(doc_key)
            return ValidateCodeResponseDTO(
                success=False,
                message="Usuario no encontrado.",
            )

        self.repository.delete_user_code(doc_key)

        usuario_prisma = (user.get("UsuarioPrisma") or user.get("UsuarioTyT") or "").strip()
        password_prisma = (user.get("ContrasenaPRISMA") or user.get("ContraseñaTyT") or "").strip()

        return ValidateCodeResponseDTO(
            success=True,
            message=None,
            usuario_prisma=usuario_prisma or None,
            password_prisma=password_prisma or None,
        )