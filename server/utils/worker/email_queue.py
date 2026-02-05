import json

from config.redis.config_redis import get_redis_client
from utils.worker.constants import QUEUE_EMAIL_CREDENTIALS


def push_email_credentials_task(to_address: str, doc_key: str, code: str) -> None:
    payload = {
        "to": to_address,
        "doc_key": doc_key,
        "code": code,
    }
    client = get_redis_client()
    client.lpush(QUEUE_EMAIL_CREDENTIALS, json.dumps(payload))
