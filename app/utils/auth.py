
from fastapi import Header, HTTPException, Security
from app.utils.redis_key_helper import isValidRedisKeyTTL
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
bearer_scheme = HTTPBearer()


"""
async def isValidLoggedInUserSessionToken(authorization: str = Header(..., alias="Authorization")):
    # return True
    # print(f"authorization: {authorization}")
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing authorization header."
        )
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header format."
        )
    # Extract token
    token = authorization.replace("Bearer ", "").strip()
    keyName = f"UserLoggedInSessionToken-{token}"
    # Validate Redis TTL
    if not isValidRedisKeyTTL(keyName):
        raise HTTPException(
            status_code=401,
            detail="Session token is invalid or expired."
        )
    return {"is_valid": True}
"""
    

def isValidLoggedInUserSessionToken(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    # return True
    token = credentials.credentials.replace("Bearer ", "").strip()
    keyName = f"UserLoggedInSessionToken-{token}"
    # Validate Redis TTL
    if not isValidRedisKeyTTL(keyName):
        raise HTTPException(
            status_code=401,
            detail="Session token is invalid or expired."
        )
    return True    
   