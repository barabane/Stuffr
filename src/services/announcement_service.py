from src.repositories.announcement_repository import get_announcement_repository
from src.schemas.announcement_schemas import get_announcement_schemas
from src.services.base_service import BaseService


class AnnouncementService(BaseService):
    def __init__(self, repository, schemas):
        super().__init__(repository=repository, schemas=schemas)


def get_announcement_service() -> AnnouncementService:
    return AnnouncementService(
        repository=get_announcement_repository(), schemas=get_announcement_schemas()
    )
