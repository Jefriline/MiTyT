import json
import os
import time

import redis

from config.redis.config_redis import get_redis_client
from utils.gmail_send import send_email
from utils.worker.constants import QUEUE_EMAIL_CREDENTIALS

_RECONNECT_DELAY_SECONDS = 2
_CONNECTION_ERRORS = (
    redis.ConnectionError,
    redis.TimeoutError,
    OSError,
    BrokenPipeError,
    ConnectionResetError,
)

_EMAIL_TEMPLATE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "credentials_email.html"
)


def _load_email_body(code: str) -> str:
    site_url = (os.getenv("SITE_URL") or "").strip().rstrip("/")
    logo_block = ""
    if site_url:
        logo_url = f"{site_url}/static/img/logoSena.png"
        logo_block = (
            f'<img src="{logo_url}" alt="SENA" '
            'style="height:48px; width:auto; display:block; margin:0 auto;" />'
        )
    try:
        with open(_EMAIL_TEMPLATE_PATH, encoding="utf-8") as file:
            template = file.read()
    except OSError:
        template = (
            "<p>Tu código de seguridad es: <strong>{{ code }}</strong></p>"
            "<p>Introduce este código en la página para ver tus credenciales.</p>"
        )
    return template.replace("{{ code }}", code).replace(
        "{{ logo_block }}", logo_block
    )


def _process_one_message(payload_str: str) -> None:
    payload = json.loads(payload_str)
    to_address = (payload.get("to") or "").strip()
    doc_key = (payload.get("doc_key") or "").strip()
    code = (payload.get("code") or "").strip()
    if not to_address or not code:
        print(f"[Worker] Mensaje ignorado: faltan datos (to={bool(to_address)}, code={bool(code)})")
        return

    print(f"[Worker] Enviando código a {to_address[:4]}***@... (doc: {doc_key[:4]}***)")
    subject = "Código de seguridad - Credenciales TyT"
    body_html = _load_email_body(code)
    send_email(to_address=to_address, subject=subject, body_html=body_html)
    print(f"[Worker] Correo enviado exitosamente a {to_address[:4]}***@...")


def run_email_worker(poll_timeout_seconds: int = 5) -> None:
    messages_processed = 0
    client = None

    while True:
        try:
            if client is None:
                print("[Worker] Conectando a Redis...")
                client = get_redis_client()
                print(f"[Worker] Conectado. Escuchando cola '{QUEUE_EMAIL_CREDENTIALS}'...")

            result = client.brpop(QUEUE_EMAIL_CREDENTIALS, timeout=poll_timeout_seconds)
            if result is None:
                continue
            _queue_name, payload_str = result
            messages_processed += 1
            print(f"[Worker] Mensaje #{messages_processed} recibido, procesando...")
            _process_one_message(payload_str)

        except _CONNECTION_ERRORS as connection_error:
            print(f"[Worker] Conexión perdida con Redis ({type(connection_error).__name__}), reconectando en {_RECONNECT_DELAY_SECONDS}s...")
            try:
                if client is not None:
                    client.close()
            except Exception:
                pass
            client = None
            time.sleep(_RECONNECT_DELAY_SECONDS)

        except json.JSONDecodeError as decode_error:
            print(f"[Worker] ERROR: Mensaje inválido en cola: {decode_error}")
        except Exception as error:
            print(f"[Worker] ERROR procesando correo: {error}")
            time.sleep(1)
