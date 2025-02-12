from abc import ABC

import pydantic
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.base_model import BaseModel
from src.utils.decorators import logger_decorator


class BaseRepository(ABC):
    def __init__(self, model: BaseModel):
        self.model: BaseModel = model

    @logger_decorator
    async def add(self, entity: pydantic.BaseModel, session: AsyncSession):
        return await self._execute_scalar_one_or_none(
            query=insert(self.model)
            .values(**entity.model_dump())
            .returning(self.model),
            session=session,
        )

    @logger_decorator
    async def get_one(
        self, entity_id: int | str, session: AsyncSession
    ) -> BaseModel | None:
        return await self._execute_scalar_one_or_none(
            query=select(self.model).where(self.model.id == entity_id), session=session
        )

    @logger_decorator
    async def get_all(self, session: AsyncSession):
        return await self._execute_scalars_all(
            query=select(self.model), session=session
        )

    @logger_decorator
    async def update(
        self, entity_id: int | str, entity: pydantic.BaseModel, session: AsyncSession
    ):
        return await self._execute_scalar_one_or_none(
            query=update(self.model)
            .where(self.model.id == entity_id)
            .values(**entity.model_dump())
            .returning(self.model),
            session=session,
        )

    @logger_decorator
    async def delete(self, entity_id: int | str, session: AsyncSession):
        await self._execute_without_result(
            query=delete(self.model).where(self.model.id == entity_id), session=session
        )

    async def delete_all(self, session: AsyncSession):
        await self._execute_without_result(query=delete(self.model), session=session)

    async def _execute_scalar_one_or_none(self, query, session: AsyncSession):
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def _execute_scalars_all(self, query, session: AsyncSession):
        result = await session.execute(query)
        return result.scalars().all()

    async def _execute_without_result(self, query, session: AsyncSession):
        await session.execute(query)


def get_base_repository() -> BaseRepository:
    return BaseRepository(model=BaseModel)
