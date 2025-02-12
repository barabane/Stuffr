import math
import time
from functools import wraps
from typing import Callable

from src.logging import LogDecoratorScheme, logger


def logger_decorator(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        response = await func(*args, **kwargs)

        duration = math.ceil((time.time() - start_time) * 1000)
        logger.info(
            LogDecoratorScheme(
                func_method_name=func.__name__, duration=duration
            ).model_dump_json(indent=2)
        )
        return response

    return wrapper
