from fastapi import APIRouter, status
from login_api import services
from login_api.pydantic_models import User, Token, Credentials, OTP

from login_api.logger import logger
from login_api.globals import Globals


login_router = APIRouter()


@login_router.post("/register/user", status_code=status.HTTP_201_CREATED, response_model=User)
async def register_user(user: User):
    log_request("POST /register/user", f"nickname={user.username}")
    return await services.register_user(user=user.dict())


@login_router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login_user(credentials: Credentials):
    log_request("POST /login", f"username={credentials.username}")
    return await services.perform_login(credentials=credentials.dict())


@login_router.post("/login2fa", status_code=status.HTTP_200_OK, response_model=Token)
async def login_user_2fa(otp: OTP):
    log_request("POST /login", f"username={otp.username}")
    return await services.check_user_otp(otp=otp.dict())


def log_request(endpoint: str, _id: str = None):
    logger.info(f'{endpoint} for {_id} : request_id={Globals().get_value("request_id")}'
                if _id else f'{endpoint} : request_id={Globals().get_value("request_id")}')
