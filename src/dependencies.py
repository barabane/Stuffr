from datetime import datetime

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
from src.utils.token_manager import TokenManager


async def get_current_user(response: Response, request: Request) -> User | None:
    session: AsyncSession
    async with session_maker() as session:
        try:
            if not request.cookies.get('stuffr_access', None):
                raise UnauthorizedException
            payload = TokenManager.decode_token(token=request.cookies['stuffr_access'])

            user: User | None = await session.get(User, payload['sub'])
            if datetime.fromtimestamp(payload['exp']) < datetime.now():
                payload = TokenManager.decode_token(
                    token=request.cookies['stuffr_refresh']
                )
                if datetime.fromtimestamp(payload['exp']) < datetime.now():
                    raise ExpiredSignatureError
                user.refresh_tokens.remove(['stuffr_refresh'])

                access_token, refresh_token = TokenManager.get_tokens(
                    {
                        'sub': str(user.id),
                    }
                )

                response.set_cookie(
                    key='stuffr_access',
                    value=access_token,
                    secure=True,
                    httponly=True,
                    samesite='strict',
                )
                response.set_cookie(
                    key='stuffr_refresh',
                    value=refresh_token,
                    secure=True,
                    httponly=True,
                    samesite='strict',
                )
                user.refresh_tokens.append(refresh_token)

            return user
        except ExpiredSignatureError:
            logger.error('Token expired error')
            response.delete_cookie('stuffr_access')
            response.delete_cookie('stuffr_refresh')
            raise TokenExpiredException
        except InvalidKeyError:
            logger.error('Invalid token error')
            response.delete_cookie('stuffr_access')
            response.delete_cookie('stuffr_refresh')
            raise GetTokenException
