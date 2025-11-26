
from fastapi import Header
from app.utils.redis_key_helper import isValidRedisKeyTTL


def isValidLoggedInUserSessionToken(authorization: str = Header(None)):
    return True
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split("Bearer ")[1].strip()
        keyName = f"UserLoggedInSessionToken-{token}"
        return isValidRedisKeyTTL(keyName)
    else:
        return False
    
    