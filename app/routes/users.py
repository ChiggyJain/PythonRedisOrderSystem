
from fastapi import APIRouter
from app.redis_client import r
from app.config import SESSION_TTL_SECONDS
from uuid import uuid4
from app.utils.response import ok

router = APIRouter()

@router.post("/login")
def login(username: str):
    # create a simple session token in Redis with TTL
    token = uuid4().hex
    r.set(f"session:{token}", username, ex=SESSION_TTL_SECONDS)
    return ok({"token": token}, "Logged in")
