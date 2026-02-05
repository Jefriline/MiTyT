import os

import redis


def get_redis_client() -> redis.Redis:
    url = (os.getenv("REDIS_URL") or "redis://localhost:6379").strip()
    return redis.from_url(url, decode_responses=True)
