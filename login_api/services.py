import jwt
import random
from string import ascii_letters, digits
from pymysql import Error as PyMySqlError
from cryptography.fernet import Fernet
from pymemcache.client.base import Client as CacheClient
from login_api.dao import execute_no_result_query, execute_single_result_query
from login_api.config import current_config
from login_api.pydantic_models import Token, User
from login_api.adapters import adapt_email_to_user_query, adapt_username_to_user_query, \
    adapt_user_to_token_data, adapt_token_to_model, adapt_user_creation_to_query, adapt_db_user_to_model
from login_api.exception import ApiException
from login_api.logger import logger


async def get_user(query: str):
    try:
        result = await execute_single_result_query(query=query, conf=current_config.DB)
    except PyMySqlError as ex:
        logger.error(f"Database Error: {ex}")
        raise ApiException(code=500, message="Internal Server Error")

    return result


def encrypt_password(f: Fernet, password: str):
    return f.encrypt(bytes(password, 'utf-8'))


def decrypt_password(f: Fernet, password: bytes):
    return (f.decrypt(password)).decode("utf-8")


async def create_user(user: dict):
    try:
        result = await execute_no_result_query(
            query=adapt_user_creation_to_query(user=user),
            conf=current_config.DB
        )
    except PyMySqlError as ex:
        logger.error(f"Database Error: {ex}")
        raise ApiException(code=500, message="Internal Server Error")

    return result


async def check_new_user(query: str, check_field: str):
    if await get_user(query=query):
        logger.error(f"Database Error: {check_field} already used")
        raise ApiException(code=409, message=f"{check_field} already used")


def create_jwt(payload: dict):
    return {
        'token': jwt.encode(payload, current_config.JWT_SECRET, algorithm=current_config.JWT_ALG),
        'type': 'JWT'
    }


def generate_otp():
    source = ascii_letters + digits
    return ''.join(random.choice(source) for i in range(current_config.OTP_LEN))


def send_user_otp(email: str, otp: str):
    logger.info(f"[{email}] OTP = {otp}")
    print(f"[{email}] OTP = {otp}")


def set_cache_item(cache_key: str, cache_value: str):
    cache = CacheClient((current_config.CACHE['HOST'], current_config.CACHE['PORT']))
    cache.set(cache_key, cache_value)


def get_cache_item(cache_key: str):
    cache = CacheClient((current_config.CACHE['HOST'], current_config.CACHE['PORT']))

    return cache.get(cache_key)


def delete_cache_item(cache_key: str):
    cache = CacheClient((current_config.CACHE['HOST'], current_config.CACHE['PORT']))
    cache.delete(cache_key)


def handle_2fa_login(email: str, username: str):
    otp = generate_otp()
    send_user_otp(email=email, otp=otp)
    set_cache_item(cache_key=username, cache_value=otp)

    return {
        'token': '',
        'type': '2FA'
    }


def check_password(db_password: bytes, password: str):
    my_fernet = Fernet(current_config.DB_SECRET)
    clean_db_password = decrypt_password(f=my_fernet, password=db_password)
    if clean_db_password != password:
        logger.error(f"Invalid password: {password}")
        raise ApiException(code=401, message="Invalid password")


async def register_user(user: dict) -> User:
    query = adapt_email_to_user_query(email=user['email'])
    await check_new_user(query=query, check_field="Email")
    query = adapt_username_to_user_query(username=user['username'])
    await check_new_user(query=query, check_field="Username")
    my_fernet = Fernet(current_config.DB_SECRET)
    user['password'] = encrypt_password(f=my_fernet, password=user['password']).decode()
    await create_user(user=user)
    saved_user = await get_user(query=query)
    saved_user['password'] = decrypt_password(f=my_fernet, password=bytes(saved_user['password']))

    return adapt_db_user_to_model(name=saved_user['name'], surname=saved_user['surname'],
                                  username=saved_user['username'], email=saved_user['email'],
                                  password=saved_user['password'], secure_auth=saved_user['secure_auth'])


async def perform_login(credentials: dict) -> Token:
    query = adapt_username_to_user_query(username=credentials['username'])
    db_user = await get_user(query=query)
    if not db_user:
        logger.error(f"Invalid username: {credentials['username']}")
        raise ApiException(code=401, message="Invalid username")
    check_password(db_password=bytes(db_user['password']), password=credentials['password'])
    if db_user['secure_auth']:
        result = handle_2fa_login(email=db_user['email'], username=db_user['username'])
    else:
        result = create_jwt(adapt_user_to_token_data(username=db_user['username']))

    return adapt_token_to_model(token=result['token'], token_type=result['type'])


async def check_user_otp(otp: dict):
    cache_otp = (get_cache_item(otp['username'])).decode()
    if cache_otp != otp['password']:
        logger.error(f"Invalid OTP: {otp['password']}")
        raise ApiException(code=401, message="Invalid OTP")

    result = create_jwt(adapt_user_to_token_data(username=otp['username']))

    return adapt_token_to_model(token=result['token'], token_type=result['type'])
