
from app.redis_client import redisConObj
import json
from app.config import PUBSUB_CHANNEL

def notify_order_created(order_id: str, user_id: str):
    payload = {"order_id": order_id, "user_id": user_id}
    redisConObj.publish(PUBSUB_CHANNEL, json.dumps(payload))
