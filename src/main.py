from fastapi import FastAPI, Request
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.config import settings
from src.middlewares.logging_middleware import logging_middleware
from src.routers.announcement_router import announcement_router
from src.routers.user_router import user_router
from src.utils.cache import redis_cache


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await redis_cache.init(url=settings.REDIS_URL)
    yield
    await redis_cache.close()


app = FastAPI(title='Stuffr 🐶', lifespan=lifespan)


@app.exception_handler(500)
async def internal_server_error_custom_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    return JSONResponse(
        status_code=500, content={'details': 'Ошибка на стороне сервера'}
    )


app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)

app.include_router(user_router)
app.include_router(announcement_router)
