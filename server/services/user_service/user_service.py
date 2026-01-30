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
