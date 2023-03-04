import logging
from login_api.config.common_settings import CommonSettings


class DockerSettings(CommonSettings):
    ENV = "docker"
    LOG_LEVEL = logging.DEBUG
    DB = {
        "HOST": "db_login",
        "DB": "login_api",
        "USER": "root",
        "PASSWORD": "password"
    }
    CACHE = {
        "HOST": "memcached",
        "PORT": "11211"
    }
