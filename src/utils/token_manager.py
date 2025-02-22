from datetime import datetime, timedelta

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from src.config import settings
from src.exceptions import GetTokenException, TokenExpiredException


class TokenManager:
    @staticmethod
    def get_reset_token(payload: dict):
        payload['exp'] = datetime.now() + timedelta(
            minutes=settings.RESET_TOKEN_EXPIRATION
        )
        return jwt.encode(
            payload, settings.TOKEN_SECRET, algorithm=settings.TOKEN_ALGORITHM
        )

    @staticmethod
    def get_tokens(payload: dict) -> tuple[str, str]:
        payload['exp'] = datetime.now() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRATION
        )
        access_token = jwt.encode(
            payload, settings.TOKEN_SECRET, algorithm=settings.TOKEN_ALGORITHM
        )
        payload['exp'] = datetime.now() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRATION
        )
        refresh_token = jwt.encode(
            payload, settings.TOKEN_SECRET, algorithm=settings.TOKEN_ALGORITHM
        )
        return access_token, refresh_token

    @staticmethod
    def decode_token(token: str):
        try:
            payload = jwt.decode(
                token,
                settings.TOKEN_SECRET,
                algorithm=settings.TOKEN_ALGORITHM,
                algorithms=[settings.TOKEN_ALGORITHM],
            )

            if datetime.fromtimestamp(payload['exp']) < datetime.now():
                raise ExpiredSignatureError

            return payload
        except ExpiredSignatureError:
            raise TokenExpiredException
        except InvalidTokenError:
            raise GetTokenException
