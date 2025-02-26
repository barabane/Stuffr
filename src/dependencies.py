from fastapi import Request, Response
from jwt.exceptions import ExpiredSignatureError, InvalidKeyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import session_maker
from src.database.models.user_model import User
from src.exceptions import (
    GetTokenException,
    TokenExpiredException,
    UnauthorizedException,
)
from src.logging import logger
from src.utils.cache import redis_cache
from src.utils.token_manager import TokenManager


async def get_current_user(response: Response, request: Request) -> User | None:
    try:
        async with session_maker() as session:
            if not request.cookies.get('stuffr_access', None):
                raise UnauthorizedException
            payload = TokenManager.decode_token(token=request.cookies['stuffr_access'])
            user: User | None = await session.get(User, payload['sub'])
            return user
    except ExpiredSignatureError:
        session: AsyncSession
        async with session_maker() as session:
            try:
                payload = TokenManager.decode_token(
                    token=request.cookies['stuffr_refresh']
                )
            except ExpiredSignatureError:
                logger.error('Token expired error')
                user: User | None = await session.get(User, payload['sub'])
                user.refresh_tokens.remove(request.cookies['stuffr_refresh'])
                await session.commit()
                raise TokenExpiredException

            user: User | None = await session.get(User, payload['sub'])
            access_token, refresh_token = TokenManager.set_tokens(
                {
                    'sub': str(user.id),
                },
                response=response,
            )
            user.refresh_tokens.remove(request.cookies['stuffr_refresh'])
            user.refresh_tokens.append(refresh_token)
            await session.commit()
            user: User | None = await session.get(User, payload['sub'])
            return user
    except InvalidKeyError:
        logger.error('Invalid token error')
        raise GetTokenException


async def get_cache():
    yield redis_cache
