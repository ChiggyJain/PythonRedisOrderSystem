

from app.redis_client import redisConObj
from app.lua_scripts import decr_stock_script
from app.utils.response import err
import uuid

STOCK_KEY_PREFIX = "Stock:" 
ORDER_ID_PREFIX = "Order:"

def stock_key(product_id: str) -> str:
    return f"{STOCK_KEY_PREFIX}{product_id}"

def create_order_id() -> str:
    return f"{ORDER_ID_PREFIX}{uuid.uuid4().hex}"

def check_stock(product_id: str) -> int:
    val = redisConObj.get(stock_key(product_id))
    if val is None:
        return -1
    return int(val)

def decrement_stock_lua(product_id: str, qty: int):
    """
    Use cached Lua script for atomic check + decrement.
    Returns dict with success + order_id if success.
    Return codes from Lua:
      -2 -> key missing
      -1 -> insufficient stock
      >=0 -> remaining stock after decrement
    """
    key = stock_key(product_id)
    res = decr_stock_script(keys=[key], args=[qty])
    # res is either int or string depending on redis-py; ensure int
    res = int(res)
    if res == -2:
        return {"success": False, "message": "Product not found"}
    if res == -1:
        return {"success": False, "message": "Insufficient stock"}
    # success: create order id
    order_id = create_order_id()
    return {"success": True, "order_id": order_id, "remaining_stock": res}

# Optional: WATCH approach (slower) - shown for reference
def decrement_stock_watch(product_id: str, qty: int, max_retries: int = 5):
    key = stock_key(product_id)
    for attempt in range(max_retries):
        try:
            redisConObj.watch(key)
            val = redisConObj.get(key)
            if val is None:
                redisConObj.unwatch()
                return {"success": False, "message": "Product not found"}
            current = int(val)
            if current < qty:
                redisConObj.unwatch()
                return {"success": False, "message": "Insufficient stock"}
            new = current - qty
            pipe = redisConObj.pipeline()
            pipe.multi()
            pipe.set(key, new)
            result = pipe.execute()
            # if execute succeeds, result is truthy
            order_id = create_order_id()
            return {"success": True, "order_id": order_id, "remaining_stock": new}
        except Exception as e:
            # WatchError will cause retry
            continue
    return {"success": False, "message": "Could not acquire lock, try again"}
