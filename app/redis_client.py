
import redis
from .config import REDIS_HOST, REDIS_PORT

# single redis client to be imported across app
redisConObj = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
