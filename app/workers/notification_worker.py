
import json
from app.redis_client import redisConObj
from app.config import PUBSUB_CHANNEL

def run_notification_listener():
    pubsub = redisConObj.pubsub()
    pubsub.subscribe(PUBSUB_CHANNEL)
    print("Notification listener subscribed to", PUBSUB_CHANNEL)
    for msg in pubsub.listen():
        if msg["type"] == "message":
            payload = json.loads(msg["data"])
            # simulate sending email/push
            print("[notification] Send notification for order:", payload.get("order_id"))
