
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.exceptions import HTTPException
from app.redis_client import redisConObj
from app.routes import users as users_router
from app.routes import products as products_router
from app.routes import orders as orders_router
from app.utils.response import standard_http_response


app = FastAPI(title="Python Redis Order System")
app.include_router(users_router.router, prefix="/users", tags=["users"])
app.include_router(products_router.router, prefix="/products", tags=["products"])
app.include_router(orders_router.router, prefix="/orders", tags=["orders"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = []
    for err in exc.errors():
        field = ".".join(err["loc"][1:])
        msg = err["msg"]
        error_messages.append(f"{field}: {msg}")
    return standard_http_response(status_code=422, messages=error_messages)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return standard_http_response(status_code=exc.status_code, messages=[exc.detail])


@asynccontextmanager
async def lifespan(app):
    print(f"Connecting to redis...")
    pong = redisConObj.ping()
    print(f"Redis connected successfully: {pong}")
    yield
    print("Closing redis connection...")
    redisConObj.close()
    print("Closed redis connection...")


@app.get("/system-health", summary="System Health")
async def check_system_health():
    """
        This API is used to check system health status only.
    """
    return standard_http_response(status_code=200, messages=["System is up and running"])
