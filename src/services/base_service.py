from abc import ABC
from typing import List

import pydantic
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.base_model import BaseModel
from src.repositories.base_repository import BaseRepository, get_base_repository
from src.schemas.base_schemas import BaseSchemas, get_base_schemas
from src.utils.decorators import logger_decorator


class BaseService(ABC):
    def __init__(self, repository: BaseRepository, schemas: BaseSchemas) -> BaseModel:
        self.repository: BaseRepository = repository
        self.schemas: BaseSchemas = schemas

    @logger_decorator
    async def add(self, entity: pydantic.BaseModel, session: AsyncSession) -> BaseModel:
        return await self.repository.add(entity=entity, session=session)

    @logger_decorator
    async def get_one(
        self, entity_id: int | str, session: AsyncSession
    ) -> BaseModel | None:
        return await self.repository.get_one(entity_id=entity_id, session=session)

    @logger_decorator
    async def get_all(
        self, session: AsyncSession, filters: dict = None
    ) -> List[BaseModel]:
        return await self.repository.get_all(filters=filters, session=session)

    @logger_decorator
    async def update(
        self, entity_id: int | str, entity: pydantic.BaseModel, session: AsyncSession
    ):
        return await self.repository.update(
            entity_id=entity_id, entity=entity, session=session
        )

    @logger_decorator
    async def delete(self, entity_id: int | str, session: AsyncSession):
        return await self.repository.delete(entity_id=entity_id, session=session)

    @logger_decorator
    async def delete_all(self, session: AsyncSession):
        return await self.repository.delete_all(session=session)


def get_base_service() -> BaseService:
    return BaseService(repository=get_base_repository(), schemas=get_base_schemas())
