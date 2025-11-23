import logging
from functools import wraps
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")


def initialization(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args, **kwargs):
        module_name = func.__module__
        logging.debug(f"↳ Extension {module_name} loaded.")
        return func(*args, **kwargs)

    return wrapper


def deletion(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args, **kwargs):
        module_name = func.__module__
        logging.debug(f"↳ Extension {module_name} removed.")
        return func(*args, **kwargs)

    return wrapper
