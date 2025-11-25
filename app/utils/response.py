

from fastapi import HTTPException
from fastapi.responses import JSONResponse

def ok(data=None, message="OK"):
    return JSONResponse({"success": True, "message": message, "data": data})

def err(status_code=400, message="Error"):
    raise HTTPException(status_code=status_code, detail=message)
