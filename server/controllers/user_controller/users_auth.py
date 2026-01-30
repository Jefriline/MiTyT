
from services.user_service.user_service import UserService

class ControllerAuth:
    def __init__(self) -> None:
        self.user_service = UserService()

    def is_authenticated(self, username, password) -> bool:
        try:
            result = self.user_service.login_user(username, password)
            return result
        except Exception as e:
            print(f"Excepción: {e}")
            return False

