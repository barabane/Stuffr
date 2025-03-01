from sqlalchemy import delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.announcement_model import Announcement
from src.database.models.user_favorite_model import UserFavorite
from src.database.models.user_model import User
from src.exceptions import UserForbiddenException
from src.logging import LogMessageScheme, logger
from src.repositories.announcement_repository import get_announcement_repository
from src.schemas.announcement_schemas import (
    AnnouncementStatus,
    get_announcement_schemas,
)
from src.services.base_service import BaseService
from src.utils.decorators import logger_decorator


class AnnouncementService(BaseService):
    def __init__(self, repository, schemas):
        super().__init__(repository=repository, schemas=schemas)

    @logger_decorator
    async def archive_announcement(self, announcement_id: str, session: AsyncSession):
        announcement: Announcement = await session.get(
            self.repository.model, announcement_id
        )
        announcement.status = AnnouncementStatus.ARCHIVED.value

    @logger_decorator
    async def approve(
        self, announcement_id: str, user: User, session: AsyncSession
    ) -> Announcement:
        announcement: Announcement = await session.get(
            self.repository.model, announcement_id
        )
        announcement.status = AnnouncementStatus.PUBLISHED.value
        logger.info(
            LogMessageScheme(
                message=(
                    f'Объявление id={announcement_id} '
                    f'опубликовано администратором id={user.id}'
                )
            ).model_dump_json(indent=2)
        )
        return announcement

    @logger_decorator
    async def decline(
        self, announcement_id: str, user: User, session: AsyncSession
    ) -> Announcement:
        announcement: Announcement = await session.get(
            self.repository.model, announcement_id
        )
        announcement.status = AnnouncementStatus.DECLINE.value
        logger.info(
            LogMessageScheme(
                message=(
                    f'Объявление id={announcement_id} '
                    f'отправлено на доработку администратором id={user.id}'
                )
            ).model_dump_json(indent=2)
        )
        return announcement

    @logger_decorator
    async def add_to_favorite(
        self, announcement_id: str, user: User, session: AsyncSession
    ):
        await self.repository._execute_without_result(
            query=insert(UserFavorite).values(
                user_id=user.id, announcement_id=announcement_id
            ),
            session=session,
        )

    @logger_decorator
    async def delete_from_favorite(
        self, announcement_id: str, user: User, session: AsyncSession
    ):
        await self.repository._execute_without_result(
            query=delete(UserFavorite).where(
                UserFavorite.user_id == user.id,
                UserFavorite.announcement_id == announcement_id,
            ),
            session=session,
        )

    @logger_decorator
    async def unpublish(self, announcement_id: str, user: User, session: AsyncSession):
        announcement: Announcement = await session.get(
            self.repository.model, announcement_id
        )

        if announcement.user_id != user.id:
            raise UserForbiddenException

        announcement.status = AnnouncementStatus.UNPUBLISHED.value
        return announcement


def get_announcement_service() -> AnnouncementService:
    return AnnouncementService(
        repository=get_announcement_repository(), schemas=get_announcement_schemas()
    )
