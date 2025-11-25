
from fastapi import FastAPI
from app.utils.response import standard_http_response
from app.routes import users as users_router
from app.routes import products as products_router
#from app.routes import orders as orders_router


app = FastAPI(title="Python Redis Order System")


app.include_router(users_router.router, prefix="/users", tags=["users"])
app.include_router(products_router.router, prefix="/products", tags=["products"])
#app.include_router(orders_router.router, prefix="/orders", tags=["orders"])



@app.get("/system-health", summary="System Health")
def check_system_health():
    """
        This API is used to check system health status only.
    """
    return standard_http_response(status_code=200, messages=["System is up and running"], data={})
