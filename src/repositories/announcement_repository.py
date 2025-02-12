from src.database.models.announcement_model import Announcement
from src.repositories.base_repository import BaseRepository


class AnnouncementRepository(BaseRepository):
    def __init__(self, model):
        super().__init__(model=model)


def get_announcement_repository() -> AnnouncementRepository:
    return AnnouncementRepository(model=Announcement)
