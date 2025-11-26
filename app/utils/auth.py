
from fastapi import Header, HTTPException
from app.utils.redis_key_helper import isValidRedisKeyTTL


def isValidLoggedInUserSessionToken(authorization: str = Header(None)):
    return True
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header."
        )
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid Authorization header format."
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
    return True

    
    