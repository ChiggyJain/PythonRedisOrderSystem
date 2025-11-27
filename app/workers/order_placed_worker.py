
import time
import json
from app.redis_client import redisConObj
from app.utils.response import standard_response, standard_http_response



def createOrderPlacedStreamConsumerGroupInRedis():
    """
        Create the consumer group for the 'Order-Placed-Stream' in Redis.
        - If the stream does not exist, `mkstream=True` will create it automatically.
        - If the consumer group already exists, the function will not throw an error.
        - Returns a standardized response object.
    """
    orderPlacedStreamName = "Order-Placed-Stream"
    orderPlacedGroupName = "Order-Placed-Group"
    createdOrderPlacedStreamConsumerGroupInRedisRspObj = standard_response(status_code=400, messages=["Failed to create consumer group."])
    try:
        createdOrderPlacedStreamConsumerGroupInRedisResult = redisConObj.xgroup_create(orderPlacedStreamName, orderPlacedGroupName, id="0", mkstream=True)
        if createdOrderPlacedStreamConsumerGroupInRedisResult:
            createdOrderPlacedStreamConsumerGroupInRedisRspObj['status_code'] = 200
            createdOrderPlacedStreamConsumerGroupInRedisRspObj['messages'] = [f"Consumer group '{orderPlacedGroupName}' created successfully for stream '{orderPlacedStreamName}'."]
    except Exception as e:
        if "BUSYGROUP" in str(e):
            createdOrderPlacedStreamConsumerGroupInRedisRspObj["status_code"] = 200
            createdOrderPlacedStreamConsumerGroupInRedisRspObj["messages"] = [
                f"Consumer group '{orderPlacedGroupName}' already exists for stream '{orderPlacedStreamName}'."
            ]
        else:
            createdOrderPlacedStreamConsumerGroupInRedisRspObj["status_code"] = 500
            createdOrderPlacedStreamConsumerGroupInRedisRspObj["messages"] = [f"Redis error: {str(e)}"]      
    return createdOrderPlacedStreamConsumerGroupInRedisRspObj


def run_worker(poll_interval=1.0):
    createOrderPlacedStreamConsumerGroupInRedis()
    pass