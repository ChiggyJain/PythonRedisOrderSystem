
from fastapi import APIRouter, HTTPException, Depends
from app.services.stock_service import decrement_stock_lua
from app.services.order_stream_service import add_order_event
from app.services.rate_limit_service import is_rate_limited
from app.utils.response import ok, err

router = APIRouter()

def check_rate(user_id: str = "anon"):
    # for demo: max 5 requests per 60 sec
    if is_rate_limited(user_id, max_requests=5, window_seconds=60):
        raise HTTPException(status_code=429, detail="Too many requests")

@router.post("/")
def place_order(user_id: str, product_id: str, qty: int, depends=Depends(check_rate)):
    # validate
    if qty <= 0:
        return err(400, "qty must be > 0")

    # atomic decrement via Lua
    res = decrement_stock_lua(product_id, qty)
    if not res["success"]:
        return err(400, res["message"])

    order_id = res["order_id"]
    add_order_event(order_id, user_id, product_id, qty)
    return ok({"order_id": order_id, "remaining_stock": res.get("remaining_stock")}, "Order placed")
