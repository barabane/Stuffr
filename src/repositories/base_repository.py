from abc import ABC

import pydantic
from sqlalchemy import and_, delete, insert, select, update
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
    async def get_all(self, session: AsyncSession, filters: dict = None):
        query = select(self.model)

        if not filters:
            return await self._execute_scalars_all(query=query, session=session)

        offset = filters.get('offset', None)
        limit = filters.get('limit', None)
        order_by = filters.get('sort_by')
        if offset:
            del filters['offset']
        if limit:
            del filters['limit']
        if order_by:
            del filters['sort_by']

        filters = self.__process_filters(filters=filters)
        query = query.filter(*filters)
        if order_by:
            query = query.order_by(getattr(self.model, order_by))

        if offset:
            query = query.offset(offset)

        if limit:
            query = query.limit(limit)

        return await self._execute_scalars_all(query=query, session=session)

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

    def __process_filters(self, filters: dict):
        result_filters = []

        if filters.get('price_min', None) and filters.get('price_max', None):
            result_filters.append(
                and_(
                    getattr(self.model, 'price') >= filters.get('price_min'),
                    getattr(self.model, 'price') <= filters.get('price_max'),
                )
            )
        elif filters.get('price_min', None):
            result_filters.append(
                getattr(self.model, 'price') >= filters.get('price_min')
            )
        elif filters.get('price_max', None):
            result_filters.append(
                getattr(self.model, 'price') <= filters.get('price_max')
            )

        for key, value in filters.items():
            if value and hasattr(self.model, key):
                result_filters.append(getattr(self.model, key) == value)

        return result_filters


def get_base_repository() -> BaseRepository:
    return BaseRepository(model=BaseModel)
