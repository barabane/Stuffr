from datetime import datetime, timedelta

import jwt
import pytz
from fastapi import Response

from src.config import settings


class TokenManager:
    @staticmethod
    def get_reset_token(payload: dict):
        payload['exp'] = datetime.now(tz=pytz.timezone(pytz.utc.zone)) + timedelta(
            minutes=settings.RESET_TOKEN_EXPIRATION
        )
        return jwt.encode(
            payload, settings.TOKEN_SECRET, algorithm=settings.TOKEN_ALGORITHM
        )

    @staticmethod
    def set_tokens(payload: dict, response: Response) -> tuple[str, str]:
        payload['exp'] = datetime.now(tz=pytz.timezone(pytz.utc.zone)) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRATION
        )
        access_token = jwt.encode(
            payload, settings.TOKEN_SECRET, algorithm=settings.TOKEN_ALGORITHM
        )

        response.set_cookie(
            key='stuffr_access',
            value=access_token,
            secure=True,
            httponly=True,
            samesite='strict',
        )

        payload['exp'] = datetime.now(tz=pytz.timezone(pytz.utc.zone)) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRATION
        )
        refresh_token = jwt.encode(
            payload, settings.TOKEN_SECRET, algorithm=settings.TOKEN_ALGORITHM
        )

        response.set_cookie(
            key='stuffr_refresh',
            value=refresh_token,
            secure=True,
            httponly=True,
            samesite='strict',
        )

        return access_token, refresh_token

    @staticmethod
    def decode_token(token: str):
        payload = jwt.decode(
            token,
            settings.TOKEN_SECRET,
            algorithm=settings.TOKEN_ALGORITHM,
            algorithms=[settings.TOKEN_ALGORITHM],
        )
        return payload
