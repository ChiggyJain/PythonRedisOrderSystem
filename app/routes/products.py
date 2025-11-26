
from fastapi import APIRouter
from fastapi import Depends
from app.utils.auth import isValidLoggedInUserSessionToken
from app.utils.response import standard_response, standard_http_response
from app.schemas.products_schema import *
from app.utils.redis_key_helper import *


productsList = [
    {
        "productId" : 11,
        "productName" : "Shampoo",
        "productAvailableStockQty" : 11
    },
    {
        "productId" : 12,
        "productName" : "Detol Soap",
        "productAvailableStockQty" : 12
    },
    {
        "productId" : 13,
        "productName" : "Tooth Paste",
        "productAvailableStockQty" : 13
    }
]

def getDummyProductIdWiseDetails(productsList):
    return {item["productId"]: item for item in productsList}

def prepareProductsDetailsToSetKeyValueObjCacheEntriesInRedisViaPipeline(productsList):
    return {"Product-ID-"+str(item["productId"]): item for item in productsList}



router = APIRouter()
@router.get("/", summary="Fetch all Products Details")
async def get_all_products(isValidSessionToken:bool=Depends(isValidLoggedInUserSessionToken)):
    """
        Retrieve the complete list of available products.
        This endpoint returns all products along with their basic details such as
        product ID, product name, and available stock quantity.
        **Requirements**
        - A valid logged-in session token must be provided in request-headers.
        **Notes**
        - If the session token is invalid or expired, the request will be rejected.
        - This API does not require any path parameters.
    """
    productsRspObj = standard_response(status_code=404, messages=["Products not found."])
    try:
        global productsList
        bulkProductSetCacheRedisEntries = prepareProductsDetailsToSetKeyValueObjCacheEntriesInRedisViaPipeline(productsList)
        redisPipelineExecutedRspObj = bulkSetKeyValueObjCacheEntriesInRedisViaPipeline(bulkProductSetCacheRedisEntries)
        productsRspObj['status_code'] = 200
        productsRspObj['messages'] = [f"Products found successfully."]
        productsRspObj['data'] = productsList
    except Exception as e:
        productsRspObj['status_code'] = 500
        productsRspObj['messages'] = [f"An error occured: {str(e)}"]
    return standard_http_response(status_code=productsRspObj["status_code"], messages=productsRspObj['messages'], data=productsRspObj['data'])    


@router.get("/{product_id}", summary="Fetch single product details")
async def get_product_details(params:ProductDetailRequest=Depends(), isValidSessionToken:bool=Depends(isValidLoggedInUserSessionToken)):
    """
        Retrieve the details of a specific product.
        This endpoint returns detailed information about a single product based on the product ID provided in the request path.
        **Requirements**
        - A valid logged-in session token must be provided in request-headers.
        **Parameters**
        - `product_id` (path): Unique ID of the product whose details are required.
        **Notes**
        - If the session token is invalid or expired, the request will be rejected.
        - If the product ID does not exist, an appropriate error message will be returned.
    """
    productRspObj = standard_response(status_code=404, messages=["Product not found."])
    try:
        productId = params.product_id
        redisCacheEntriesKeyName = f"Product-ID-{productId}"
        productRedisCachedEntriesRspObj = getKeyValueObjRedisCacheEntries(redisCacheEntriesKeyName)
        if productRedisCachedEntriesRspObj['status_code'] == 200:
            productRspObj['status_code'] = 200
            productRspObj['messages'] = [f"Product found successfully."]
            productRspObj['data'] = productRedisCachedEntriesRspObj['data']
        else:
            global productsList
            productIdWiseDetails = getDummyProductIdWiseDetails(productsList)
            if productId in productIdWiseDetails:
                productRspObj['status_code'] = 200
                productRspObj['messages'] = [f"Product found successfully."]
                productRspObj['data'] = [productIdWiseDetails[productId]]
    except Exception as e:
        productRspObj['status_code'] = 500
        productRspObj['messages'] = [f"An error occured: {str(e)}"]
    return standard_http_response(status_code=productRspObj["status_code"], messages=productRspObj['messages'], data=productRspObj['data'])   


@router.post("/setstock", summary="Update single product stock qunatity details")
async def update_product_stock_details(params:ProductStockRequest, isValidSessionToken:bool=Depends(isValidLoggedInUserSessionToken)):
    """
        Update the stock quantity of a specific product.
        This endpoint updates the available stock quantity for a given product
        based on the details provided in the request body.
        **Requirements**
        - A valid logged-in session token must be provided in the request headers.
        **Request Body**
        - `product_id`: The unique ID of the product whose stock needs to be updated.
        - `stock_quantity`: The new stock quantity to set for the product.
        **Notes**
        - If the session token is invalid or expired, the request will be rejected.
        - If the product ID does not exist, an appropriate error message will be returned.
        - Only authenticated users are allowed to perform stock updates.
    """
    print(f"update_product_stock_details params: {params}")
    productRspObj = standard_response(status_code=404, messages=["Product stock quantity not updated."])
    try:
        global productsList
        productId = params.product_id
        productStockQuantity = params.stock_quantity
        redisCacheEntriesKeyName = f"Product-ID-{productId}"
        productIdWiseDetails = getDummyProductIdWiseDetails(productsList)
        productIdWiseDetails[productId]['productAvailableStockQty'] = productStockQuantity
        if productId in productIdWiseDetails:
            productsList = list(productIdWiseDetails.values())
            bulkProductSetCacheRedisEntries = prepareProductsDetailsToSetKeyValueObjCacheEntriesInRedisViaPipeline([productIdWiseDetails[productId]])
            redisPipelineExecutedRspObj = bulkSetKeyValueObjCacheEntriesInRedisViaPipeline(bulkProductSetCacheRedisEntries)
            productRspObj['status_code'] = 200
            productRspObj['messages'] = [f"Product stock quantity details is updated successfully."]
            productRspObj['data'] = [productIdWiseDetails[productId]]
        else:
            productRspObj['status_code'] = 404
            productRspObj['messages'] = [f"Given product_id does not exists."]
    except Exception as e:
        productRspObj['status_code'] = 500
        productRspObj['messages'] = [f"An error occured: {str(e)}"]
    return standard_http_response(status_code=productRspObj["status_code"], messages=productRspObj['messages'], data=productRspObj['data'])   
