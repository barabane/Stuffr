import http
import math
import time

from fastapi import Request, Response

from src.logging import LogEndpointScheme, logger


class LoggingMiddleware:
    async def __call__(self, request: Request, call_next, *args, **kwargs):
        start_time = time.time()
        exception_object = None

        try:
            response = await call_next(request)
        except Exception as ex:
            response_body = bytes(http.HTTPStatus.INTERNAL_SERVER_ERROR.phrase.encode())
            response = Response(
                content=response_body,
                status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR.real,
            )
            exception_object = ex

        duration: int = math.ceil((time.time() - start_time) * 1000)
        message = LogEndpointScheme(
            request_path=str(request.url),
            request_method=request.method,
            response_status_code=response.status_code,
            remote_ip=request.client[0],
            duration=duration,
        ).model_dump_json(indent=2)

        if exception_object:
            logger.error(message)
            raise exception_object

        logger.info(message)
        return response


logging_middleware = LoggingMiddleware()
