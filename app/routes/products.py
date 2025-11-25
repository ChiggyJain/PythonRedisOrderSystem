
from fastapi import APIRouter, HTTPException
from app.services.cache_service import get_product_from_cache, set_product_cache
from app.services.stock_service import stock_key, check_stock
from app.utils.response import ok, err
from app.redis_client import r

router = APIRouter()

@router.get("/{product_id}")
def get_product(product_id: str):
    cached = get_product_from_cache(product_id)
    if cached:
        return ok(cached, message="Product (cache)")
    # Simulate DB read: here we use Redis hash to represent product master
    master_key = f"product_master:{product_id}"
    data = r.hgetall(master_key)
    if not data:
        return err(404, "Product not found")
    set_product_cache(product_id, data)
    return ok(data, "Product (master)")

@router.post("/{product_id}/setstock")
def set_stock(product_id: str, qty: int):
    if qty < 0:
        return err(400, "qty must be >= 0")
    r.set(stock_key(product_id), qty)
    return ok({"product_id": product_id, "stock": qty}, "Stock updated")
