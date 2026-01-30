from pydantic import BaseModel


class UserRowDTO(BaseModel):
    nombre: str
    edad: int


class UserUploadResponseDTO(BaseModel):
    inserted_count: int
    total_rows: int
    errors: list[str]
