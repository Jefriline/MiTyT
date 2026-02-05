from functools import wraps

from flask import jsonify, request

from config.redis.config_redis import get_redis_client
from utils.excel_aprendiz.normalize import normalize_document_key
from utils.worker.constants import RATE_LIMIT_KEY_PREFIX, RATE_LIMIT_TTL_SECONDS


def _get_document_from_request() -> str | None:
    if request.is_json:
        body = request.get_json(silent=True) or {}
        return (body.get("document") or "").strip()
    return (request.form.get("document") or "").strip()


def validate_credentials_rate_limit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        document = _get_document_from_request()
        doc_key = normalize_document_key(document) if document else None
        if not doc_key:
            return jsonify({"success": False, "message": "Documento inválido."}), 400

        redis_client = get_redis_client()
        rate_key = f"{RATE_LIMIT_KEY_PREFIX}{doc_key}"
        was_set = redis_client.set(
            rate_key,
            "1",
            ex=RATE_LIMIT_TTL_SECONDS,
            nx=True,
        )
        if not was_set:
            ttl = redis_client.ttl(rate_key)
            seconds_remaining = max(1, ttl)
            return jsonify({
                "success": False,
                "message": "Debes esperar antes de solicitar otro código.",
                "blocked": True,
                "seconds_remaining": seconds_remaining,
            }), 429

        return func(*args, **kwargs)

    return wrapper
