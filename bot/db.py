import os
from redis.asyncio import from_url


REDIS_URL = (
    os.getenv("REDIS_URL")
    or os.getenv("UPSTASH_REDIS_URL")
    or "rediss://default:ATl7AAIjcDEwYjdkZjhmYTczNjk0YzZmOWY4Zjg0ODE4NmU1YTcwN3AxMA@ideal-pegasus-14715.upstash.io:6379"
)


redis = from_url(
    REDIS_URL,
    decode_responses=True,
    # --- hardening ---
    health_check_interval=30,   # ping on idle conns
    socket_keepalive=True,      # TCP keep-alive
    retry_on_timeout=True,
    socket_timeout=5,           # I/O timeout
    socket_connect_timeout=5,   # connect timeout
    max_connections=20,
)
