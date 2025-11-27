import pytest
import multiprocessing
import time
from app.redis_client import redisConObj
from fastapi.testclient import TestClient
from app.main import app
from app.config import ORDER_PLACED_STREAM, ORDER_PLACED_GROUP
from app.workers.order_placed_worker import runOrderPlacedStreamConsumerGroupWorker1

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def redis_setup_and_cleanup():
    
    print("\n=== BEFORE ALL TESTS: Connecting to Redis ===")
    pong = redisConObj.ping()
    print(f"\nRedis connected successfully: {pong}")
    redisConObj.flushall()
    print("\nRedis FLUSHALL executed (before tests)")

    yield

    print("\n=== AFTER ALL TESTS: Closing Redis ===")
    redisConObj.flushall()
    print("\nRedis FLUSHALL executed (after tests)")
    redisConObj.close()
    print("\nClosed redis connection...")


@pytest.fixture(scope="session")
def auth_token():
    print("\n=== Fake auth token is generating ===")
    token = "Test123"
    keyName = f"UserLoggedInSessionToken-{token}"
    redisConObj.setex(keyName, 300, "1")
    print(f"\n=== Fake auth token {token} is generated and stored in redis cached ===")
    return token


@pytest.fixture(scope="session", autouse=True)
def start_and_stop_order_placed_worker():

    print("\n=== Starting Order Placed Worker ===")
    worker_process = multiprocessing.Process(target=runOrderPlacedStreamConsumerGroupWorker1)
    worker_process.start()
    
    yield

    print("\n=== Stopping order placed worker ===")
    wait_until_no_pending_order_placed_events(ORDER_PLACED_STREAM, ORDER_PLACED_GROUP)
    worker_process.terminate()
    worker_process.join(timeout=1)
    print("\nOrder placed worker stopped successfully")


def wait_until_no_pending_order_placed_events(orderPlacedStreamName, orderPlacedGroupName):
    try:
        print("\n=== Inside func:wait_until_no_pending_order_placed_events ===")
        while True:
            pendingOrderPlacedEvents = redisConObj.xpending(orderPlacedStreamName, orderPlacedGroupName)
            if pendingOrderPlacedEvents and pendingOrderPlacedEvents["pending"]>0:
                print(f"\nStill pending order-placed-events: {pendingOrderPlacedEvents}")
                time.sleep(1)
            else:
                print(f"\nNo pending order-placed-events")
                break
    except Exception as e:
        pass