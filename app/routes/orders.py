
from fastapi import APIRouter
from fastapi import Depends
from uuid import uuid4
import time
import copy
from app.utils.auth import isValidLoggedInUserSessionToken
from app.utils.response import standard_response, standard_http_response
from app.schemas.orders_schema import *
from app.utils.redis_key_helper import *
from app.routes.products import (
    productsList, 
    getDummyProductIdWiseDetails, 
    prepareProductsDetailsToSetKeyValueObjCacheEntriesInRedisViaPipeline
)
from app.config import *

router = APIRouter()

@router.post("/place-order", summary="Place single product order details")
def place_single_product_order_details(params:OrderPlaceRequest, isValidSessionToken:bool=Depends(isValidLoggedInUserSessionToken)):
    """
        Place an order for a specific product.
        This endpoint creates a new order by reducing the product’s available stock
        based on the quantity provided in the request body.
        - **Requirements**
            - A valid logged-in session token must be provided in the request headers.
        - **Request Body**
            - `product_id`: The unique ID of the product for which the order is being placed.
            - `stock_quantity`: The quantity of the product to order.
        - **Notes**
            - If the session token is invalid or expired, the request will be rejected.
            - If the product ID does not exist, an appropriate error message will be returned.
            - If sufficient stock is not available, the order will not be processed.
            - Only authenticated users are allowed to place orders.
    """
    placedOrderRspObj = standard_response(status_code=404, messages=["Product not found."])
    try:
        global productsList
        productId = int(params.product_id)
        productStockQuantity = int(params.stock_quantity)
        productIdWiseDetails = getDummyProductIdWiseDetails(productsList)
        if productId in productIdWiseDetails:
            if int(productIdWiseDetails[productId]['productAvailableStockQty'])>productStockQuantity:
                maxRequest = 5
                windowSeconds = 60
                redisRateLimiterKeyName = f"RL:UserID:111+ProductID:{productId}+T:{int(time.time() // windowSeconds)}" 
                fixedWindowRedisRateLimiterRspObj = fixedWindowRedisRateLimiter(redisRateLimiterKeyName, maxRequest, windowSeconds)
                if fixedWindowRedisRateLimiterRspObj['status_code'] == 200:
                    createdNewOrderId = uuid4().hex
                    # deducting product-stock-quantity
                    productIdWiseDetails[productId]['productAvailableStockQty']-= productStockQuantity
                    productsList = list(productIdWiseDetails.values())
                    # storing updated product-stock-quantity at two levels [In-Redis-Memory, In-Memory-Dict]
                    bulkProductSetCacheRedisEntries = prepareProductsDetailsToSetKeyValueObjCacheEntriesInRedisViaPipeline([productIdWiseDetails[productId]])
                    redisPipelineExecutedRspObj = bulkSetKeyValueObjCacheEntriesInRedisViaPipeline(bulkProductSetCacheRedisEntries)
                    # adding placed-order event-data into redis stream for background processing details via (worker)
                    orderPlacedRedisStreamName = ORDER_PLACED_STREAM
                    orderPlacedEventData = copy.deepcopy(productIdWiseDetails[productId])
                    orderPlacedEventData['orderId'] = createdNewOrderId
                    orderPlacedEventData['purchaseProductStockQty'] = productStockQuantity
                    addedEventDataInRedisStreamRspObj = addEventDataInRedisStream(orderPlacedRedisStreamName, orderPlacedEventData)
                    
                    ## for testing purpose only
                    """

                        #time.sleep(1)
                        #addedEventDataInRedisStreamRspObj = addEventDataInRedisStream(orderPlacedRedisStreamName, orderPlacedEventData)
                        #time.sleep(1)
                        #addedEventDataInRedisStreamRspObj = addEventDataInRedisStream(orderPlacedRedisStreamName, orderPlacedEventData)
                        #time.sleep(1)
                        #addedEventDataInRedisStreamRspObj = addEventDataInRedisStream(orderPlacedRedisStreamName, orderPlacedEventData)

                        # from app.workers.order_placed_worker import runOrderPlacedStreamConsumerGroupWorker1
                        # runOrderPlacedStreamConsumerGroupWorker1()

                        # from app.workers.order_placed_worker import createOrderPlacedStreamConsumerGroupInRedis
                        # createOrderPlacedStreamConsumerGroupInRedis()

                    """
    
                    # dumping response
                    placedOrderRspObj['status_code'] = 200
                    placedOrderRspObj['messages'] = [f"Order placed successfully."]
                    placedOrderRspObj['data'] = {
                        "orderId" : createdNewOrderId
                    }
                    
                else:
                    placedOrderRspObj['status_code'] = fixedWindowRedisRateLimiterRspObj['status_code']
                    placedOrderRspObj['messages'] = fixedWindowRedisRateLimiterRspObj['messages']                    
            else:
                placedOrderRspObj['messages'] = [f"Order not placed due to insufficient product quantity."]
        else:
            placedOrderRspObj['status_code'] = 404
            placedOrderRspObj['messages'] = [f"Given product_id does not exists to place the order details."]
    except Exception as e:
        placedOrderRspObj['status_code'] = 500
        placedOrderRspObj['messages'] = [f"An error occured: {str(e)}"]
    return standard_http_response(status_code=placedOrderRspObj["status_code"], messages=placedOrderRspObj['messages'], data=placedOrderRspObj['data'])   
    
