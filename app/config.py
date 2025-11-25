
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
ORDER_STREAM = os.getenv("ORDER_STREAM", "Orders-Stream")
ORDER_GROUP = os.getenv("ORDER_GROUP", "Orders-Group")
ORDER_CONSUMER = os.getenv("ORDER_CONSUMER", "Order-Worker-1")
PUBSUB_CHANNEL = os.getenv("PUBSUB_CHANNEL", "Order-Notifications")
PRODUCT_CACHE_PREFIX = "Product:"
RATE_LIMIT_KEY = "Rate:"
SESSION_TTL_SECONDS = 3600
