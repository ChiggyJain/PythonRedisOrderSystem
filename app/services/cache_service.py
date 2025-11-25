
from app.redis_client import redisConObj
from app.config import PRODUCT_CACHE_PREFIX
import json

# 5 minutes
CACHE_TTL = 60*5  

def product_cache_key(product_id: str) -> str:
    return f"{PRODUCT_CACHE_PREFIX}{product_id}"

def get_product_from_cache(product_id: str):
    key = product_cache_key(product_id)
    raw = redisConObj.get(key)
    if raw:
        # store JSON string for complex objects
        return json.loads(raw)
    return None

def set_product_cache(product_id: str, product_obj: dict):
    key = product_cache_key(product_id)
    redisConObj.set(key, json.dumps(product_obj), ex=CACHE_TTL)

def bulk_set_products(products: dict):
    """
    products: {product_id: product_obj}
    use pipelines for speed
    """
    pipe = redisConObj.pipeline()
    for pid, pobj in products.items():
        pipe.set(product_cache_key(pid), json.dumps(pobj), ex=CACHE_TTL)
    pipe.execute()
