from fastapi import Request

from src.logging import logger


class LoggingMiddleware:
    async def __call__(self, request: Request, call_next):
        logger.info(f'Call {request.url}')
        return await call_next(request)


logging_middleware = LoggingMiddleware()
