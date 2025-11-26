
import json
from app.redis_client import redisConObj
from app.utils.response import standard_response


def isValidRedisKeyTTL(keyName:str):
    return redisConObj.ttl(keyName)>0


def bulkSetKeyValueObjCacheEntriesInRedisViaPipeline(entries: dict, ttl: int = 0):
    """
        Store multiple key-value entries in Redis using pipeline.
        entries: dict → { keyInputValue : valueObj }
        ttl: expiration time in seconds for each key.
    """
    redisPipelineExecutedRspObj = standard_response(status_code=400, messages=["Given parameters are invalid."])
    try:
        if isinstance(entries, dict):
            pipe = redisConObj.pipeline()
            for key_input, value_obj in entries.items():
                if ttl>0:
                    pipe.set(key_input, json.dumps(value_obj), ex=ttl)
                else:
                    pipe.set(key_input, json.dumps(value_obj))
            redisPipelineExecutedResultList = pipe.execute()
            redisPipelineExecutedRspObj['status_code'] = 200
            redisPipelineExecutedRspObj['messages'] = ["Bulk cache entries is set in redis."]
            redisPipelineExecutedRspObj['data'] = redisPipelineExecutedResultList
    except Exception as e:
        redisPipelineExecutedRspObj['status_code'] = 500
        redisPipelineExecutedRspObj['messages'] = [f"An error occured: {str(e)}"]
    return redisPipelineExecutedRspObj


def getKeyValueObjRedisCacheEntries(keyName):
    """
        Store multiple key-value entries in Redis using pipeline.
        entries: dict → { keyInputValue : valueObj }
        ttl: expiration time in seconds for each key.
    """
    redisKeyValueObjRspObj = standard_response(status_code=404, messages=["Given {keyName} cache entries are not found."])
    try:
        if keyName:
            keyValueObj = json.loads(redisConObj.get(keyName))
            redisKeyValueObjRspObj['status_code'] = 200
            redisKeyValueObjRspObj['messages'] = [f"Given {keyName} cache entries are found."]
            redisKeyValueObjRspObj['data'] = [keyValueObj]
    except Exception as e:
        redisKeyValueObjRspObj['status_code'] = 500
        redisKeyValueObjRspObj['messages'] = [f"An error occured: {str(e)}"]
    return redisKeyValueObjRspObj


def fixedWindowRedisRateLimiter(keyName=str, maxRequest=int, windowSeconds=int):
    """
        Apply Fixed Window Rate Limiting using Redis INCR + EXPIRE mechanism.
        **How it works**
        - Redis key represents a time window.
        - INCR increments the request counter for the window.
        - EXPIRE ensures the counter resets when the window ends.
        - If the counter exceeds `max_requests`, rate limit is triggered.
        **Parameters**
        - key_name (str): Redis key representing the fixed window bucket (e.g., "rate:user123:170000001").
        - max_requests (int): Maximum allowed requests in the window.
        - window_seconds (int): Size of the window in seconds.
    """
    fixedWindowRedisRateLimiterRspObj = standard_response(status_code=429, messages=["Too many requests. Please try again later."])
    try:
        if keyName:
            current = redisConObj.incr(keyName)
            if current == 1:
                redisConObj.expire(keyName, windowSeconds)
            if current > maxRequest:
                fixedWindowRedisRateLimiterRspObj['status_code'] = 429
                fixedWindowRedisRateLimiterRspObj['messages'] = [f"Too many requests. Please try again later."]
            else:
                fixedWindowRedisRateLimiterRspObj['status_code'] = 200
                fixedWindowRedisRateLimiterRspObj['messages'] = [f"Request allowed."]
                fixedWindowRedisRateLimiterRspObj['dtaa'] = {
                    "currentCount" : current
                }
    except Exception as e:
        fixedWindowRedisRateLimiterRspObj['status_code'] = 500
        fixedWindowRedisRateLimiterRspObj['messages'] = [f"An error occured: {str(e)}"]
    return fixedWindowRedisRateLimiterRspObj
