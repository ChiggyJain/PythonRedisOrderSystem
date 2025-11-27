
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
ORDER_STREAM = os.getenv("ORDER_PLACED_STREAM", "Order-Placed-Stream")
ORDER_GROUP = os.getenv("ORDER_PLACED_GROUP", "Order-Placed-Group")
ORDER_CONSUMER = os.getenv("ORDER_PLACED_GROUP_WORKER1", "Order-Placed-Group-Worker1")
PUBSUB_CHANNEL = os.getenv("PUBSUB_CHANNEL", "Order-Notifications")
PRODUCT_CACHE_PREFIX = "Product:"
RATE_LIMIT_KEY = "Rate:"
SESSION_TTL_SECONDS = 3600
