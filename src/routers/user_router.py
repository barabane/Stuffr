from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_async_session
from src.database.models.user_model import User
from src.dependencies import get_current_user
from src.exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserDoesNotExistsException,
)
from src.schemas.user_schemas import (
    CreateUserScheme,
    LoginUserCredentials,
    RegisterUserCredentials,
)
from src.services.user_service import UserService, get_user_service
from src.utils.password_manager import PasswordManager
from src.utils.token_manager import TokenManager

user_router = APIRouter(prefix='/user', tags=['User'])


@user_router.post('/register')
async def register_user(
    response: Response,
    user_credentials: RegisterUserCredentials,
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_async_session),
):
    user_exists: User | None = await user_service.get_by_email(
        email=user_credentials.email, session=session
    )

    raise Exception

    if user_exists:
        raise UserAlreadyExistsException

    hashed_password: bytes = PasswordManager.get_password_hash(
        password=user_credentials.password
    )
    new_user: User = await user_service.add(
        entity=CreateUserScheme(
            name=user_credentials.name,
            email=user_credentials.email,
            hashed_password=hashed_password,
        ),
        session=session,
    )

    access_token, refresh_token = TokenManager.get_tokens(
        {
            'sub': str(new_user.id),
        }
    )

    new_user.refresh_tokens.append(refresh_token)

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

    return new_user


@user_router.post('/login')
async def login_user(
    response: Response,
    user_credentials: LoginUserCredentials,
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_async_session),
):
    user: User | None = await user_service.get_by_email(
        email=user_credentials.email, session=session
    )

    if not user:
        raise UserDoesNotExistsException

    if not PasswordManager.check_password_hash(
        password=user_credentials.password, hashed=user.hashed_password
    ):
        raise InvalidCredentialsException

    access_token, refresh_token = TokenManager.get_tokens(
        {
            'sub': str(user.id),
        }
    )

    user.refresh_tokens.append(refresh_token)

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

    return user


@user_router.post('/logout')
async def logout(
    response: Response,
    request: Request,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    user.refresh_tokens.remove(request.cookies['stuffr_refresh'])

    session.add(user)
    await session.commit()
    response.delete_cookie('stuffr_access')
    response.delete_cookie('stuffr_refresh')
    return 200
