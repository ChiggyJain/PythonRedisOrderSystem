
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.redis_client import redisConObj
client = TestClient(app)


def test_check_system_health_success():
    result = client.get("/system-health")
    print(f"test_check_system_health_success resp: {result.json()}")
    rspObj = result.json()
    assert rspObj["status_code"] == 200

def test_authenticate_user_success():
    result = client.post("/users/login/", json={"username":"User1"})
    print(f"test_authenticate_user_success resp: {result.json()}")
    rspObj = result.json()
    assert rspObj["status_code"] == 200

def test_authenticate_user_failure():
    result = client.post("/users/login/", json={"username":"User3"})
    print(f"test_authenticate_user_success resp: {result.json()}")
    rspObj = result.json()
    assert rspObj["status_code"] == 401   


def test_get_all_products_success(auth_token):
    result = client.get("/products", headers={"Authorization":f"Bearer {auth_token}"})
    print(f"test_get_all_products_success resp: {result.json()}")
    rspObj = result.json()
    assert rspObj["status_code"] == 200


def test_get_all_products_failure():
    result = client.get("/products", headers={"Authorization": "Bearer 57d1813ed7d34ac892d961fa81db18a5"})
    print(f"test_get_all_products_failure resp: {result.json()}")
    rspObj = result.json()
    assert rspObj["status_code"] == 401

def test_get_product_details_success(auth_token):
    result = client.get("/products/13", headers={"Authorization":f"Bearer {auth_token}"})
    print(f"test_get_product_details_success resp: {result.json()}")
    rspObj = result.json()
    assert rspObj["status_code"] == 200

def test_get_product_details_failure(auth_token):
    result = client.get("/products/15", headers={"Authorization":f"Bearer {auth_token}"})
    print(f"test_get_product_details_failure resp: {result.json()}")
    rspObj = result.json()
    assert rspObj["status_code"] == 404 

def test_update_product_stock_details_success(auth_token):
    result = client.post("/products/setstock", headers={"Authorization":f"Bearer {auth_token}"}, json={"product_id":13, "stock_quantity":100})
    print(f"test_update_product_stock_details_success resp: {result.json()}")
    rspObj = result.json()
    assert rspObj["status_code"] == 200   

def test_get_product_details_success_after_update(auth_token):
    result = client.get("/products/13", headers={"Authorization":f"Bearer {auth_token}"})
    print(f"test_get_product_details_success_after_update resp: {result.json()}")
    rspObj = result.json()
    assert rspObj["status_code"] == 200

def test_place_single_product_order_details_failure1(auth_token):
    result = client.post("/orders/place-order", headers={"Authorization":f"Bearer {auth_token}"}, json={"product_id":13, "stock_quantity":300})
    print(f"test_place_single_product_order_details_failure1 resp: {result.json()}")
    rspObj = result.json()
    assert rspObj["status_code"]!=200

def test_place_single_product_order_details_failure2(auth_token):
    result = client.post("/orders/place-order", headers={"Authorization":f"Bearer {auth_token}"}, json={"product_id":13, "stock_quantity":-300})
    print(f"test_place_single_product_order_details_failure2 resp: {result.json()}")
    rspObj = result.json()
    assert rspObj["status_code"]!=200    

def test_place_single_product_order_details_success(auth_token):
    result = client.post("/orders/place-order", headers={"Authorization":f"Bearer {auth_token}"}, json={"product_id":13, "stock_quantity":1})
    print(f"test_place_single_product_order_details_success resp: {result.json()}")
    rspObj = result.json()
    assert rspObj["status_code"]==200

def test_get_product_details_success_after_placing_order(auth_token):
    result = client.get("/products/13", headers={"Authorization":f"Bearer {auth_token}"})
    print(f"test_get_product_details_success_after_placing_order resp: {result.json()}")
    rspObj = result.json()
    assert rspObj["status_code"] == 200