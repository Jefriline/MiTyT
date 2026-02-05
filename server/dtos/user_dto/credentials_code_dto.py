from pydantic import BaseModel, Field


class SendCodeRequestDTO(BaseModel):
    document: str = Field(..., min_length=1, max_length=50)


class ValidateCodeRequestDTO(BaseModel):
    document: str = Field(..., min_length=1, max_length=50)
    code: str = Field(..., min_length=1, max_length=20)


class SendCodeResponseDTO(BaseModel):
    success: bool
    message: str


class ValidateCodeResponseDTO(BaseModel):
    success: bool
    message: str | None = None
    usuario_prisma: str | None = None
    password_prisma: str | None = None
