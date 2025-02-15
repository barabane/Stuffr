import math
import time
from functools import wraps
from typing import Callable

from src.database.models.user_model import User
from src.exceptions import UserForbiddenException
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


def protect(role_id: int):
    def decorator_wrapper(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user: User = kwargs.get('user', None)
            if user.role_id != role_id:
                raise UserForbiddenException
            return await func(*args, **kwargs)

        return wrapper

    return decorator_wrapper
