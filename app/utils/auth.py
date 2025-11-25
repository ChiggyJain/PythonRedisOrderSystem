
from app.utils.redis_key_helper import isValidRedisKeyTTL

def isValidLoggedInUserSessionToken(token):
    keyName = f"UserLoggedInSessionToken-{token}"
    return isValidRedisKeyTTL(keyName)
    
    