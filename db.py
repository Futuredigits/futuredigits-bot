import os
from redis.asyncio import from_url


REDIS_URL = (
    os.getenv("REDIS_URL")
    or os.getenv("UPSTASH_REDIS_URL")
    or "rediss://default:ATl7AAIjcDEwYjdkZjhmYTczNjk0YzZmOWY4Zjg0ODE4NmU1YTcwN3AxMA@ideal-pegasus-14715.upstash.io:6379"
)


redis = from_url(REDIS_URL, decode_responses=True)
