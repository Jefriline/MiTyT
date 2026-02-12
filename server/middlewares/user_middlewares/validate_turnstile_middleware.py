import os
from functools import wraps

import requests
from flask import jsonify, render_template, request


SITEVERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
FORM_FIELD_TOKEN = "cf-turnstile-response"


def _get_remote_ip() -> str | None:
    remote_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if remote_ip and "," in remote_ip:
        remote_ip = remote_ip.split(",")[0].strip()
    return remote_ip or None


def _verify_turnstile_token(token: str, remote_ip: str | None) -> tuple[bool, str | None]:
    secret_key = os.getenv("TURNSTILE_KEY", "").strip()
    if not secret_key:
        return True, None

    if not token or not token.strip():
        return False, "Verificación de seguridad requerida. Completa el captcha e intenta de nuevo."

    payload = {
        "secret": secret_key,
        "response": token.strip(),
    }
    if remote_ip:
        payload["remoteip"] = remote_ip

    try:
        response = requests.post(
            SITEVERIFY_URL,
            data=payload,
            timeout=10,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        outcome = response.json()
    except requests.RequestException as request_error:
        print(f"Turnstile Siteverify request failed: {request_error}")
        return False, "No se pudo verificar la solicitud. Intenta de nuevo."
    except ValueError:
        return False, "Respuesta de verificación inválida."

    if not outcome.get("success"):
        error_codes = outcome.get("error-codes", [])
        print(f"Turnstile verification failed: {error_codes}")
        if "timeout-or-duplicate" in error_codes:
            return False, (
                "La verificación tardó demasiado o se envió dos veces. "
                "En conexiones lentas o desde celular, espera a que cargue el cuadro de verificación y vuelve a intentar."
            )
        return False, "Verificación de seguridad incorrecta. Intenta de nuevo."

    return True, None


def validate_turnstile(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.form.get(FORM_FIELD_TOKEN, "").strip()
        remote_ip = _get_remote_ip()

        is_valid, error_message = _verify_turnstile_token(token, remote_ip)
        if not is_valid:
            turnstile_site_key = os.getenv("TURNSTILE_SITE_KEY", "")
            return render_template(
                "index.html",
                user=None,
                error=error_message,
                turnstile_site_key=turnstile_site_key,
            ), 400

        return func(*args, **kwargs)

    return wrapper


def validate_turnstile_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        body = request.get_json(silent=True) or {}
        token = (body.get(FORM_FIELD_TOKEN) or "").strip()
        remote_ip = _get_remote_ip()

        is_valid, error_message = _verify_turnstile_token(token, remote_ip)
        if not is_valid:
            return jsonify({"success": False, "message": error_message}), 400

        return func(*args, **kwargs)

    return wrapper


def validate_turnstile_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.method != "POST":
            return func(*args, **kwargs)

        token = request.form.get(FORM_FIELD_TOKEN, "").strip()
        remote_ip = _get_remote_ip()

        is_valid, error_message = _verify_turnstile_token(token, remote_ip)
        if not is_valid:
            turnstile_site_key = os.getenv("TURNSTILE_SITE_KEY", "")
            return render_template(
                "login.html",
                error=error_message,
                turnstile_site_key=turnstile_site_key,
            ), 400

        return func(*args, **kwargs)

    return wrapper
