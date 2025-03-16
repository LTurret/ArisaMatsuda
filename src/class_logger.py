import logging
from functools import wraps


def initialization(func: callable) -> callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        module_name = func.__module__
        logging.debug(f"↳ Extension {module_name} loaded.")
        return func(*args, **kwargs)

    return wrapper


def deletion(func: callable) -> callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        module_name = func.__module__
        logging.debug(f"↳ Extension {module_name} removed.")
        return func(*args, **kwargs)

    return wrapper
