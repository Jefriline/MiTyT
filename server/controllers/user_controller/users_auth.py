
from dtos.user_dto.admin_dto import AdminLoginDTO
from services.user_service.user_service import UserService


class ControllerAuth:
    def __init__(self) -> None:
        self.user_service = UserService()

    def is_authenticated(self, username: str, password: str) -> bool:
        try:
            credentials = AdminLoginDTO(email=username, password=password)
            return self.user_service.login_admin(credentials)
        except Exception as error:
            print(f"Excepción: {error}")
            return False

