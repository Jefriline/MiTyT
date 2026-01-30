from copy import deepcopy

from flask import request, render_template

from services.user_service.user_service import UserService
from utils.mask_email import mask_email


class UsersSearchController:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    def handle_search(self):
        try:
            term = request.form.get("search_term", "").strip()
            if not term:
                return render_template(
                    "index.html",
                    user=None,
                    error="búsqueda vacía",
                )
            result = self.user_service.search_user(term)
            user = result.get("user", None)
            if user and isinstance(user, dict) and "Correo" in user:
                user = deepcopy(user)
                user["Correo"] = mask_email(user["Correo"])
            return render_template(
                "index.html",
                user=user,
                error=result.get("error"),
            )
        except Exception as error:
            print(f"Error en searchUsers: {error}")
            return render_template("index.html", error="Error al procesar la búsqueda")
