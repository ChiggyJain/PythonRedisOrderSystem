
from fastapi.responses import JSONResponse
from typing import List, Any

def standard_response(status_code:int=200, messages:list=None, data:Any={}):
    return {
        "status_code": status_code,
        "messages": messages,
        "data": data
    }

def standard_http_response(status_code:int=200, messages:list=None, data:Any={}, headers:dict=None):
    return JSONResponse(
        status_code=status_code,
        content=standard_response(status_code, messages, data),
        headers=headers  
    )