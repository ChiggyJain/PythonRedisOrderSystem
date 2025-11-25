
from fastapi import APIRouter
from app.utils.response import standard_response, standard_http_response
from app.schemas.login_schema import LoginRequest
from app.redis_client import redisConObj
from app.config import SESSION_TTL_SECONDS
from uuid import uuid4
dummyLoginUserNameList = {"User1", "User2"}
router = APIRouter()


@router.post("/login", summary="User Login Authentication")
def login(loginUserRequestFormData: LoginRequest):
    """
        This API validates user login credentials.
        - Provide your login username.
        - Use the sample usernames: **User1**, **User2**.
        - If the credentials are valid, the API returns an authentication token string [No JWT concept] with valid of 5 minutes only.
        - If the credentials are invalid, an appropriate error message is returned.
    """
    loginRspObj = standard_response(status_code=401, messages=["Invalid username."], data={})
    try:
        if loginUserRequestFormData.username in dummyLoginUserNameList:
            # create a simple session token in Redis with TTL
            token = uuid4().hex
            redisConObj.set(f"UserLoggedInSessionToken:{token}", loginUserRequestFormData.username, ex=SESSION_TTL_SECONDS)
            loginRspObj['status_code'] = 200
            loginRspObj['messages'] = [f"User login successfully.", "Given token is valid for 5 minutes only."]
            loginRspObj['data'] = {
                "token" : token
            }
    except Exception as e:
        loginRspObj['status_code'] = 500
        loginRspObj['messages'] = [f"Error occured: {str(e)}"]
    return standard_http_response(status_code=loginRspObj["status_code"], messages=loginRspObj['messages'], data=loginRspObj['data'])    
