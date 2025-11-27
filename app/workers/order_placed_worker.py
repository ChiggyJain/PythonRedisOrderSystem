
import time
import json
from app.redis_client import redisConObj
from app.utils.response import standard_response, standard_http_response
from app.config import *



def createOrderPlacedStreamConsumerGroupInRedis():
    """
        Create the consumer group for the 'Order-Placed-Stream' in Redis.
        - If the stream does not exist, `mkstream=True` will create it automatically.
        - If the consumer group already exists, the function will not throw an error.
        - Returns a standardized response object.
    """
    orderPlacedStreamName = ORDER_PLACED_STREAM
    orderPlacedGroupName = ORDER_PLACED_GROUP
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
            createdOrderPlacedStreamConsumerGroupInRedisRspObj["messages"] = [f"An error occured: {str(e)}"]
    return createdOrderPlacedStreamConsumerGroupInRedisRspObj


def runOrderPlacedStreamConsumerGroupWorker1(pollInterval=1.0):
    try:
        orderPlacedStreamName = ORDER_PLACED_STREAM
        orderPlacedGroupName = ORDER_PLACED_GROUP
        orderPlacedGroupWorker1Name = ORDER_PLACED_GROUP_WORKER1
        createOrderPlacedStreamConsumerGroupInRedis()
        print(f"Worker {orderPlacedGroupWorker1Name} is reading events from stream {orderPlacedStreamName} of consumer group {orderPlacedGroupName}")
        while True:
            try:
                entries = redisConObj.xreadgroup(orderPlacedGroupName, orderPlacedGroupWorker1Name, {orderPlacedStreamName: ">"}, count=5, block=2000)
                if not entries:
                    time.sleep(pollInterval)
                    continue
                for stream_name, items in entries:
                    for event_id, event_data in items:
                        print(f"Stream-Name: {orderPlacedStreamName}, Group-Name: {orderPlacedGroupName}, Worker-Name: {orderPlacedGroupWorker1Name}, Event-ID: {event_id}, Event-Data: {event_data}")
                        # acknowledging streaming event
                        redisConObj.xack(orderPlacedStreamName, orderPlacedGroupName, event_id)
                        print(f"Processed stream events and acknowledged to this Event-ID: {event_id}")
            except Exception as e:
                print(f"An error occured: {str(e)}")
                time.sleep(pollInterval)
    except Exception as e:
        print(f"An error occured: {str(e)}")
        pass