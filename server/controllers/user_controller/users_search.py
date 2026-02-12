import os
from copy import deepcopy

from flask import request, render_template

from services.user_service.user_service import UserService
from utils.excel_aprendiz.normalize import normalize_document_key
from utils.mask_email import mask_email


def _turnstile_site_key() -> str:
    return os.getenv("TURNSTILE_SITE_KEY", "")


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
                    turnstile_site_key=_turnstile_site_key(),
                )
            result = self.user_service.search_user(term)
            user = result.get("user", None)
            if not user and result.get("error") == "Usuario no encontrado":
                doc_key = normalize_document_key(term)
                print(
                    f"[search] no encontrado: raw_len={len(term)} raw_repr={repr(term)} doc_key={repr(doc_key)}"
                )
            if user and isinstance(user, dict):
                user = deepcopy(user)
                if "CorreoPersonal" in user:
                    user["CorreoPersonal"] = mask_email(user["CorreoPersonal"])
                if "Correo" in user:
                    user["Correo"] = mask_email(user["Correo"])
            return render_template(
                "index.html",
                user=user,
                error=result.get("error"),
                turnstile_site_key=_turnstile_site_key(),
            )
        except Exception as error:
            print(f"Error en searchUsers: {error}")
            return render_template(
                "index.html",
                error="Error al procesar la búsqueda",
                turnstile_site_key=_turnstile_site_key(),
            )
