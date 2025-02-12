from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from starlette.middleware.base import BaseHTTPMiddleware

from src.middlewares.logging_middleware import logging_middleware
from src.routers.user_router import user_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield


app = FastAPI(title='Stuffr 🐶', lifespan=lifespan)

app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)

app.include_router(user_router)
