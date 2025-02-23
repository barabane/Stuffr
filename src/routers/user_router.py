from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database.database import get_async_session
from src.database.models.user_model import User
from src.dependencies import get_current_user
from src.exceptions import (
    GetTokenException,
    InvalidCredentialsException,
    PasswordsNotMatchException,
    UserAlreadyExistsException,
    UserDoesNotExistsException,
)
from src.schemas.user_schemas import (
    ChangePasswordCredentials,
    CreateUserScheme,
    LoginUserCredentials,
    RegisterUserCredentials,
)
from src.services.user_service import UserService, get_user_service
from src.task_queue.worker import send_forgot_password_msg, send_reset_password_msg
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

    if user_exists:
        raise UserAlreadyExistsException

    hashed_password: bytes = PasswordManager.get_password_hash(
        password=user_credentials.password
    )
    new_user: User = await user_service.add(
        entity=CreateUserScheme(
            name=user_credentials.name,
            second_name=user_credentials.second_name,
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


@user_router.post('/forgot_password')
async def forgot_password(
    email: EmailStr,
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_async_session),
):
    user: User = await user_service.get_by_email(email=email, session=session)

    if not user:
        raise UserDoesNotExistsException

    reset_token = TokenManager.get_reset_token(payload={'sub': str(user.id)})

    send_forgot_password_msg.delay(email, settings.RESET_PASSWORD_URL + reset_token)

    return JSONResponse(
        content=f'Письмо для сброса пароля отправлено на почту {email}', status_code=201
    )


@user_router.get('/check_token')
async def check_token(
    token: str,
):
    data = TokenManager.decode_token(token=token)

    if not data['sub']:
        raise GetTokenException


@user_router.post('/reset_password')
async def reset_password(
    token: str,
    password_credentials: ChangePasswordCredentials,
    user_service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_async_session),
):
    data = TokenManager.decode_token(token=token)

    if password_credentials.new_password != password_credentials.repeat_new_password:
        raise PasswordsNotMatchException

    user: User = await user_service.reset_password(
        user_id=data['sub'],
        new_password=password_credentials.new_password,
        repeat_new_password=password_credentials.repeat_new_password,
        session=session,
    )

    send_reset_password_msg.delay(user.email)

    return user_service.schemas.get_scheme(**user.__dict__)


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
