import uuid
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl

from src.schemas.base_schemas import BaseSchemas


class LoginUserCredentials(BaseModel):
    email: EmailStr = Field(max_length=50)
    password: str = Field(min_length=8, max_length=20)


class RegisterUserCredentials(LoginUserCredentials):
    name: str = Field(min_length=3, max_length=30)
    second_name: Optional[str] = Field(min_length=3, max_length=30, default=None)


class ChangePasswordCredentials(BaseModel):
    new_password: str = Field(min_length=8, max_length=20)
    repeat_new_password: str = Field(min_length=8, max_length=20)


class GetUserScheme(BaseModel):
    id: str | uuid.UUID
    name: str = Field(min_length=3, max_length=30)
    second_name: Optional[str] = Field(min_length=3, max_length=30, default=None)
    avatar_url: Optional[HttpUrl] = None
    rating: Optional[float] = None
    email: EmailStr = Field(max_length=50)
    phone: Optional[str] = Field(max_length=20, default=None)


class CreateUserScheme(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    second_name: Optional[str] = Field(min_length=3, max_length=30, default=None)
    avatar_url: Optional[HttpUrl] = None
    role_id: Optional[int] = Field(ge=1, default=1)
    rating: Optional[float] = None
    phone: Optional[str] = Field(max_length=20, default=None)
    email: EmailStr = Field(max_length=50)
    hashed_password: str
    refresh_tokens: List[str] = []


class UpdateUserScheme(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    second_name: Optional[str] = Field(min_length=3, max_length=30, default=None)
    avatar_url: Optional[HttpUrl] = None
    phone: Optional[str] = Field(max_length=20, default=None)
    email: EmailStr = Field(max_length=50)
    refresh_tokens: List[str] = []


class UserSchemas(BaseSchemas):
    def __init__(
        self, get_scheme: BaseModel, create_scheme: BaseModel, update_scheme: BaseModel
    ):
        self.get_scheme = get_scheme
        self.create_scheme = create_scheme
        self.update_scheme = update_scheme


def get_user_schemas() -> UserSchemas:
    return UserSchemas(
        get_scheme=GetUserScheme,
        create_scheme=CreateUserScheme,
        update_scheme=UpdateUserScheme,
    )
