import pytest
from app.redis_client import redisConObj
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def redis_setup_and_cleanup():
    
    print("\n=== BEFORE ALL TESTS: Connecting to Redis ===")
    pong = redisConObj.ping()
    print(f"Redis connected successfully: {pong}")
    redisConObj.flushall()
    print("Redis FLUSHALL executed (before tests)")

    yield

    print("\n=== AFTER ALL TESTS: Closing Redis ===")
    #redisConObj.flushall()
    print("Redis FLUSHALL executed (after tests)")
    #redisConObj.close()
    print("Closed redis connection...")


@pytest.fixture(scope="session")
def auth_token():
    print("\n=== Fake auth token is generating ===")
    token = "Test123"
    keyName = f"UserLoggedInSessionToken-{token}"
    redisConObj.setex(keyName, 300, "1")
    print(f"=== Fake auth token {token} is generated and stored in redis cached ===")
    return token