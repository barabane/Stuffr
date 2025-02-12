from datetime import datetime, timedelta

import jwt

from src.config import settings


class TokenManager:
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
        return jwt.decode(
            token,
            settings.TOKEN_SECRET,
            algorithm=settings.TOKEN_ALGORITHM,
            algorithms=[settings.TOKEN_ALGORITHM],
        )
