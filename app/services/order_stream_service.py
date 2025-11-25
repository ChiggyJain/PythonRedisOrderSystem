
from app.redis_client import redisConObj
from app.config import ORDER_STREAM, PUBSUB_CHANNEL
import time
import json

def add_order_event(order_id: str, user_id: str, product_id: str, qty: int):
    data = {
        "order_id": order_id,
        "user_id": user_id,
        "product_id": product_id,
        "qty": qty,
        "created_at": str(int(time.time()))
    }
    # store as field->value pairs; encode complex nested as JSON if needed
    redisConObj.xadd(ORDER_STREAM, data)
    # also publish a lightweight notification for realtime listeners
    # PUBSUB_CHANNEL
    redisConObj.publish("orders_notifications", json.dumps({"order_id": order_id, "user_id": user_id}))
    return order_id
