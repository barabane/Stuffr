from functools import wraps
from typing import Callable

from src.logging import logger


def logger_decorator(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f'Call {func.__name__}\nWith parameters: {args, kwargs}')
        return func(*args, **kwargs)

    return wrapper
