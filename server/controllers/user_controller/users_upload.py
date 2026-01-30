from flask import request, jsonify

from dtos.user_dto.user_upload_dto import UserUploadResponseDTO
from services.user_service.user_service import UserService

class UsersUploadController:
    def __init__(self) -> None:
        self.service = UserService()

    def upload(self):
        file = request.files["file"]
        filename = file.filename or ""
        file_stream = file.read()

        result_dto = self.service.upload_excel(file_stream, filename)

        response_body = {
            "inserted_count": result_dto.inserted_count,
            "total_rows": result_dto.total_rows,
            "errors": result_dto.errors,
        }
        return jsonify(response_body), 201
    
