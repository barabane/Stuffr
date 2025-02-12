from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.announcement_model import Announcement
from src.database.models.user_model import User
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
    async def approve(self, announcement_id: str, user: User, session: AsyncSession):
        announcement: Announcement = await session.get(
            self.repository.model, announcement_id
        )
        announcement.status = AnnouncementStatus.PUBLISHED.value
        logger.info(
            LogMessageScheme(
                message=f"Объявление id={announcement_id} переведено \
                    в статус 'Опубликовано' администратором id={user.id}"
            ).model_dump_json(indent=2)
        )
        return announcement


def get_announcement_service() -> AnnouncementService:
    return AnnouncementService(
        repository=get_announcement_repository(), schemas=get_announcement_schemas()
    )
