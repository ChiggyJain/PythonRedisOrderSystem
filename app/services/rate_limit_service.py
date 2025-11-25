

from app.redis_client import redisConObj
from app.config import RATE_LIMIT_KEY
import time

def is_rate_limited(user_id: str, max_requests: int, window_seconds: int) -> bool:
    """
    Simple rate limiter using INCR+EXPIRE.
    Returns True if request should be blocked.
    """
    key = f"{RATE_LIMIT_KEY}{user_id}:{int(time.time() // window_seconds)}"
    current = redisConObj.incr(key)
    if current == 1:
        redisConObj.expire(key, window_seconds)
    return current > max_requests
