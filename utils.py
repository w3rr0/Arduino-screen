# This Python file uses the following encoding: utf-8
from functools import wraps

CONNECTED: bool = False

def if_connected(func):
    """
    Execute if there is a connection
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if CONNECTED:
            return func(*args, **kwargs)
        else:
            return None
    return wrapper
