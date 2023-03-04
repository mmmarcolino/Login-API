import logging
from login_api.config.common_settings import CommonSettings


class DevSettings(CommonSettings):
    ENV = "dev"
    LOG_LEVEL = logging.DEBUG
    DB = {
        "HOST": "127.0.0.1",
        "DB": "login_api",
        "USER": "root",
        "PASSWORD": "password"
    }
