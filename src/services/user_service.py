from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.base_model import BaseModel
from src.repositories.user_repository import get_user_repository
from src.schemas.user_schemas import get_user_schemas
from src.services.base_service import BaseService
from src.utils.decorators import logger_decorator


class UserService(BaseService):
    def __init__(self, repository, schemas):
        super().__init__(repository=repository, schemas=schemas)

    @logger_decorator
    async def get_by_email(
        self, email: EmailStr, session: AsyncSession
    ) -> BaseModel | None:
        return await self.repository.get_by_email(email=email, session=session)


def get_user_service() -> UserService:
    return UserService(repository=get_user_repository(), schemas=get_user_schemas())
