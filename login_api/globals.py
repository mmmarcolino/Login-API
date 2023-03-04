from contextvars import ContextVar
from login_api.utils import Singleton


class Globals(metaclass=Singleton):
    def __init__(self):
        self.g = ContextVar("g", default=dict())

    def reset(self):
        return self.g.set(dict())

    def get_value(self, key):
        return self.g.get().get(key)

    def set_value(self, key, value):
        old_dict = self.g.get()
        return self.g.set({**old_dict, key: value})
