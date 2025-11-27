
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
ORDER_PLACED_STREAM = os.getenv("ORDER_PLACED_STREAM", "Order-Placed-Stream")
ORDER_PLACED_GROUP = os.getenv("ORDER_PLACED_GROUP", "Order-Placed-Group")
ORDER_PLACED_GROUP_WORKER1 = os.getenv("ORDER_PLACED_GROUP_WORKER1", "Order-Placed-Group-Worker1")

