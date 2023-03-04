from login_api.config import current_config
from login_api.globals import Globals

from logging.handlers import WatchedFileHandler
from login_api import utils

import os
import logging


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = self.request_id()
        return True

    def request_id(self):
        request_id = Globals().get_value("request_id")
        if request_id:
            return request_id

        request_id = utils.generate_request_id()
        Globals().set_value("request_id", request_id)

        return request_id


def setup_logger(logger):
    if not os.path.exists(os.path.dirname(current_config.LOG_LOCATION)):
        os.makedirs(os.path.dirname(current_config.LOG_LOCATION))
    handler = WatchedFileHandler(current_config.LOG_LOCATION)
    handler.setLevel(current_config.LOG_LEVEL)
    handler.addFilter(RequestIdFilter())
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: [%(request_id)s] %(message)s "
            "[in %(pathname)s:%(lineno)d]"
        )
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


logger = logging.getLogger("AppLogger")
setup_logger(logger)
