import uuid
from typing import List

from fastapi import UploadFile
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.announcement_media_model import AnnouncementMedia
from src.database.models.announcement_model import Announcement
from src.database.models.user_favorite_model import UserFavorite
from src.database.models.user_model import User
from src.exceptions import UserForbiddenException
from src.logging import LogMessageScheme, logger
from src.repositories.announcement_repository import get_announcement_repository
from src.schemas.announcement_schemas import (
    AnnouncementStatus,
    GetAnnouncementScheme,
    get_announcement_schemas,
)
from src.services.base_service import BaseService
from src.utils.decorators import logger_decorator
from src.utils.s3 import s3_bucket


class AnnouncementService(BaseService):
    def __init__(self, repository, schemas):
        super().__init__(repository=repository, schemas=schemas)

    @logger_decorator
    async def get_all(
        self, session: AsyncSession, filters: dict = None
    ) -> List[GetAnnouncementScheme]:
        announcements: List[GetAnnouncementScheme] = [
            self.schemas.get_scheme(**announcement.__dict__)
            for announcement in await self.repository.get_all(
                filters=filters, session=session
            )
        ]

        for announcement in announcements:
            announcements_medias = await self.repository._execute_scalars_all(
                query=select(AnnouncementMedia).where(
                    AnnouncementMedia.announcement_id == announcement.id
                ),
                session=session,
            )
            announcement.medias = [media.file_url for media in announcements_medias]

        return announcements

    @logger_decorator
    async def delete(
        self,
        announcement_id: str,
        user: User,
        session: AsyncSession,
    ):
        announcement = await session.get(self.repository.model, announcement_id)

        if announcement.user_id != user.id:
            raise UserForbiddenException

        medias_urls = await self.repository._execute_scalars_all(
            query=delete(AnnouncementMedia)
            .where(AnnouncementMedia.announcement_id == announcement_id)
            .returning(AnnouncementMedia.file_url),
            session=session,
        )
        for url in medias_urls:
            await s3_bucket.delete_file(url.split('/')[-1])
        await self.repository.delete(entity_id=announcement_id, session=session)

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

    @logger_decorator
    async def add_media_to_announcement(
        self,
        announcement_id: str,
        medias: List[UploadFile],
        user: User,
        session: AsyncSession,
    ):
        medias_urls = []
        try:
            for file in medias:
                file_url = await s3_bucket.upload_file(
                    file=file,
                    name=str(uuid.uuid4()),
                )
                medias_urls.append(file_url)
                await self.repository._execute_without_result(
                    query=insert(AnnouncementMedia).values(
                        announcement_id=announcement_id, file_url=file_url
                    ),
                    session=session,
                )
        except Exception as e:
            for url in medias_urls:
                await s3_bucket.delete_file(url.split('/')[-1])
            raise e


def get_announcement_service() -> AnnouncementService:
    return AnnouncementService(
        repository=get_announcement_repository(), schemas=get_announcement_schemas()
    )
