from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.user_model import User
from src.repositories.base_repository import BaseRepository
from src.utils.decorators import logger_decorator


class UserRepository(BaseRepository):
    def __init__(self, model):
        super().__init__(model=model)

    @logger_decorator
    async def get_by_email(self, email: EmailStr, session: AsyncSession) -> User | None:
        return await self._execute_scalar_one_or_none(
            query=select(self.model).where(self.model.email == email), session=session
        )


def get_user_repository() -> UserRepository:
    return UserRepository(model=User)
