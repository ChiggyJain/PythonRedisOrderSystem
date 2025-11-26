
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
    keyValueObjRspObj = standard_response(status_code=404, messages=["Given {keyName} cache entries are not found."])
    try:
        if keyName:
            keyValueObj = json.loads(redisConObj.get(keyName))
            keyValueObjRspObj['status_code'] = 200
            keyValueObjRspObj['messages'] = [f"Given {keyName} cache entries are found."]
            keyValueObjRspObj['data'] = [keyValueObj]
    except Exception as e:
        keyValueObjRspObj['status_code'] = 500
        keyValueObjRspObj['messages'] = [f"An error occured: {str(e)}"]
    return keyValueObjRspObj
