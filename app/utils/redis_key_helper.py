
import json
from app.redis_client import redisConObj
from app.utils.response import standard_response

def isValidRedisKeyTTL(keyName:str):
    return redisConObj.ttl(keyName)>0

def bulkSetKeyValueObjCacheEntriesViaPipeline(entries: dict, ttl: int = 0):
    """
        Store multiple key-value entries in Redis using pipeline.
        entries: dict → { keyInputValue : valueObj }
        ttl: expiration time in seconds for each key.
    """
    pipelineExecutedRspObj = standard_response(status_code=401, messages=["Given entries parameters is empty OR invalid."], data={})
    try:
        if entries:
            pipe = redisConObj.pipeline()
            for key_input, value_obj in entries.items():
                if ttl>0:
                    pipe.set(key_input, json.dumps(value_obj), ex=ttl)
                else:
                    pipe.set(key_input, json.dumps(value_obj))
            pipelineExecutedResultList = pipe.execute()
            pipelineExecutedRspObj['status_code'] = 200
            pipelineExecutedRspObj['messages'] = ["Bulk cache entries is set in redis."]
            pipelineExecutedRspObj['data'] = pipelineExecutedResultList
    except Exception as e:
        pipelineExecutedRspObj['status_code'] = 500
        pipelineExecutedRspObj['messages'] = [f"An error occured: {str(e)}"]
    return pipelineExecutedRspObj

def getKeyValueObjCacheEntries(keyName):
    """
        Store multiple key-value entries in Redis using pipeline.
        entries: dict → { keyInputValue : valueObj }
        ttl: expiration time in seconds for each key.
    """
    keyValueObjRspObj = standard_response(status_code=401, messages=["Given {keyName} cache entries not found."], data={})
    try:
        if keyName:
            keyValueObj = json.load(redisConObj.get(keyName))
            keyValueObjRspObj['status_code'] = 200
            keyValueObjRspObj['messages'] = [f"Give {keyName} cache entries found."]
            keyValueObjRspObj['data'] = keyValueObj
    except Exception as e:
        keyValueObjRspObj['status_code'] = 500
        keyValueObjRspObj['messages'] = [f"An error occured: {str(e)}"]
    return keyValueObjRspObj
