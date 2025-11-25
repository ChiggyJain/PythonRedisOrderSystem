
import time
import json
from app.redis_client import redisConObj
from app.config import ORDER_STREAM, ORDER_GROUP, ORDER_CONSUMER
from app.services.pubsub_service import notify_order_created

# Ensure consumer group exists
def ensure_group():
    try:
        redisConObj.xgroup_create(ORDER_STREAM, ORDER_GROUP, id="0", mkstream=True)
    except Exception:
        pass

def process_entry(entry_id, data):
    # data fields come as strings
    # In production you'd persist to DB here; we simulate processing time
    print(f"[worker] Processing order {entry_id} -> {data}")
    # After processing, send notification
    notify_order_created(data.get("order_id"), data.get("user_id"))
    # Acknowledge
    redisConObj.xack(ORDER_STREAM, ORDER_GROUP, entry_id)

def run_worker(poll_interval=1.0):
    ensure_group()
    print("Order worker started, reading stream...")
    while True:
        try:
            entries = redisConObj.xreadgroup(ORDER_GROUP, ORDER_CONSUMER, {ORDER_STREAM: ">"}, count=5, block=2000)
            if not entries:
                # nothing new
                time.sleep(poll_interval)
                continue
            # entries = [(stream_name, [(id, {k:v}), ...])]
            for stream_name, items in entries:
                for entry_id, fields in items:
                    process_entry(entry_id, fields)
        except Exception as e:
            print("Worker error:", e)
            time.sleep(1)
