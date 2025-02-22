from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.base_model import BaseModel
from src.database.models.user_model import User
from src.exceptions import ChangePasswordException
from src.repositories.user_repository import get_user_repository
from src.schemas.user_schemas import get_user_schemas
from src.services.base_service import BaseService
from src.utils.decorators import logger_decorator
from src.utils.password_manager import PasswordManager


class UserService(BaseService):
    def __init__(self, repository, schemas):
        super().__init__(repository=repository, schemas=schemas)

    @logger_decorator
    async def get_by_email(
        self, email: EmailStr, session: AsyncSession
    ) -> BaseModel | None:
        return await self.repository.get_by_email(email=email, session=session)

    @logger_decorator
    async def reset_password(
        self,
        user_id: str,
        new_password: str,
        repeat_new_password: str,
        session: AsyncSession,
    ) -> User:
        try:
            user: User = await session.get(self.repository.model, str(user_id))

            hashed_password: bytes = PasswordManager.get_password_hash(
                password=new_password
            )
            user.hashed_password = hashed_password.decode()
        except Exception:
            await session.rollback()
            raise ChangePasswordException

        return user


def get_user_service() -> UserService:
    return UserService(repository=get_user_repository(), schemas=get_user_schemas())
