from functools import wraps

from flask import jsonify, render_template, request
import os

from config.redis.config_redis import get_redis_client
from utils.excel_aprendiz.normalize import normalize_document_key
from utils.worker.constants import (
    BRUTE_FORCE_CODE_PREFIX,
    BRUTE_FORCE_CODE_MAX_ATTEMPTS,
    BRUTE_FORCE_CODE_BLOCK_SECONDS,
    BRUTE_FORCE_LOGIN_PREFIX,
    BRUTE_FORCE_LOGIN_MAX_ATTEMPTS,
    BRUTE_FORCE_LOGIN_BLOCK_SECONDS,
)


def _get_document_from_json() -> str | None:
    body = request.get_json(silent=True) or {}
    document = (body.get("document") or "").strip()
    return normalize_document_key(document) if document else None


def _get_username_from_form() -> str | None:
    username = (request.form.get("username") or "").strip().lower()
    return username if username else None


def check_brute_force_code(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        doc_key = _get_document_from_json()
        if not doc_key:
            return jsonify({"success": False, "message": "Documento inválido."}), 400

        redis_client = get_redis_client()
        attempts_key = f"{BRUTE_FORCE_CODE_PREFIX}{doc_key}"

        current_attempts = redis_client.get(attempts_key)
        if current_attempts and int(current_attempts) >= BRUTE_FORCE_CODE_MAX_ATTEMPTS:
            ttl = redis_client.ttl(attempts_key)
            seconds_remaining = max(1, ttl)
            return jsonify({
                "success": False,
                "message": "Demasiados intentos fallidos.",
                "blocked": True,
                "seconds_remaining": seconds_remaining,
            }), 429

        return func(*args, **kwargs)

    return wrapper


def increment_brute_force_code(doc_key: str) -> dict:
    redis_client = get_redis_client()
    attempts_key = f"{BRUTE_FORCE_CODE_PREFIX}{doc_key}"

    pipe = redis_client.pipeline()
    pipe.incr(attempts_key)
    pipe.expire(attempts_key, BRUTE_FORCE_CODE_BLOCK_SECONDS)
    results = pipe.execute()
    current_attempts = results[0]

    is_blocked = current_attempts >= BRUTE_FORCE_CODE_MAX_ATTEMPTS
    seconds_remaining = None
    if is_blocked:
        ttl = redis_client.ttl(attempts_key)
        seconds_remaining = max(1, ttl)

    return {
        "attempts": current_attempts,
        "blocked": is_blocked,
        "seconds_remaining": seconds_remaining,
    }


def clear_brute_force_code(doc_key: str) -> None:
    redis_client = get_redis_client()
    attempts_key = f"{BRUTE_FORCE_CODE_PREFIX}{doc_key}"
    redis_client.delete(attempts_key)


def check_brute_force_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.method != "POST":
            return func(*args, **kwargs)

        username = _get_username_from_form()
        if not username:
            return func(*args, **kwargs)

        redis_client = get_redis_client()
        attempts_key = f"{BRUTE_FORCE_LOGIN_PREFIX}{username}"

        current_attempts = redis_client.get(attempts_key)
        if current_attempts and int(current_attempts) >= BRUTE_FORCE_LOGIN_MAX_ATTEMPTS:
            ttl = redis_client.ttl(attempts_key)
            seconds_remaining = max(1, ttl)
            turnstile_site_key = os.getenv("TURNSTILE_SITE_KEY", "")
            return render_template(
                "login.html",
                error="Cuenta bloqueada temporalmente por demasiados intentos.",
                blocked=True,
                seconds_remaining=seconds_remaining,
                turnstile_site_key=turnstile_site_key,
            ), 429

        return func(*args, **kwargs)

    return wrapper


def increment_brute_force_login(username: str) -> int:
    redis_client = get_redis_client()
    attempts_key = f"{BRUTE_FORCE_LOGIN_PREFIX}{username.lower()}"

    pipe = redis_client.pipeline()
    pipe.incr(attempts_key)
    pipe.expire(attempts_key, BRUTE_FORCE_LOGIN_BLOCK_SECONDS)
    results = pipe.execute()
    return results[0]


def clear_brute_force_login(username: str) -> None:
    redis_client = get_redis_client()
    attempts_key = f"{BRUTE_FORCE_LOGIN_PREFIX}{username.lower()}"
    redis_client.delete(attempts_key)
