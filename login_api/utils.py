from random import choice
from string import hexdigits


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def generate_request_id():
    return "".join(choice(hexdigits) for _ in range(32)).lower()
