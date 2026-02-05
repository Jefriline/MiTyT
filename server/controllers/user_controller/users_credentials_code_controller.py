from flask import request
from pydantic import ValidationError

from dtos.user_dto.credentials_code_dto import (
    SendCodeRequestDTO,
    ValidateCodeRequestDTO,
)
from middlewares.user_middlewares.validate_brute_force_middleware import (
    increment_brute_force_code,
    clear_brute_force_code,
)
from services.user_service.user_service import UserService
from utils.excel_aprendiz.normalize import normalize_document_key


class CredentialsCodeController:
    def __init__(self, user_service: UserService) -> None:
        self.service = user_service

    def send_code(self) -> tuple[dict, int]:
        try:
            body = request.get_json(silent=True) or {}
            payload = SendCodeRequestDTO.model_validate(body)
            result = self.service.send_credentials_code(payload.document)
            response = {"success": result.success, "message": result.message}
            status = 200 if result.success else 400
            return response, status
        except ValidationError:
            return {"success": False, "message": "Documento requerido."}, 400
        except Exception as error:
            print(f"CredentialsCodeController send_code: {error}")
            return {"success": False, "message": "Error al procesar la solicitud."}, 500

    def validate_code(self) -> tuple[dict, int]:
        try:
            body = request.get_json(silent=True) or {}
            payload = ValidateCodeRequestDTO.model_validate(body)
            doc_key = normalize_document_key(payload.document)
            result = self.service.validate_credentials_code(
                payload.document, payload.code
            )
            if result.success:
                clear_brute_force_code(doc_key)
                response = {
                    "success": True,
                    "message": result.message,
                    "usuario_prisma": result.usuario_prisma,
                    "password_prisma": result.password_prisma,
                }
                return response, 200

            brute_force_status = increment_brute_force_code(doc_key)
            response = {
                "success": False,
                "message": result.message,
            }
            if brute_force_status["blocked"]:
                response["blocked"] = True
                response["seconds_remaining"] = brute_force_status["seconds_remaining"]
                response["message"] = "Demasiados intentos fallidos."
                return response, 429

            return response, 400
        except ValidationError:
            return {"success": False, "message": "Documento y código requeridos."}, 400
        except Exception as error:
            print(f"CredentialsCodeController validate_code: {error}")
            return {"success": False, "message": "Error al procesar la solicitud."}, 500
