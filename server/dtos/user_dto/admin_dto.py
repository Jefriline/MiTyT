from pydantic import BaseModel, EmailStr


class AdminLoginDTO(BaseModel):
    email: EmailStr
    password: str

