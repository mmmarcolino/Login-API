from pydantic import BaseSettings
import logging


class CommonSettings(BaseSettings):
    ENV: str = ""

    LOG_LOCATION = "var/log/app.log"
    LOG_LEVEL = logging.INFO

    DB = {
        "HOST": "",
        "DB": "",
        "USER": "",
        "PASSWORD": ""
    }

    CACHE = {
        "HOST": "127.0.0.1",
        "PORT": "11211"
    }

    DB_SECRET = b'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='

    JWT_SECRET = "moebius"

    JWT_ALG = "HS256"

    OTP_LEN = 6
