
from fastapi import FastAPI
from app.routes import orders as orders_router
from app.routes import products as products_router
from app.routes import users as users_router

app = FastAPI(title="Redis Order System")

app.include_router(orders_router.router, prefix="/orders", tags=["orders"])
app.include_router(products_router.router, prefix="/products", tags=["products"])
app.include_router(users_router.router, prefix="/users", tags=["users"])

@app.get("/")
def root():
    return {"status": "ok", "service": "PythonRedisOrderSystem"}
