import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column

from .base_model import BaseModel, IdPkIntegerMixin


class AnnouncementMedia(BaseModel, IdPkIntegerMixin):
    __tablename__ = 'announcement_media'

    announcement_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('announcement.id'), nullable=False
    )
    file_url: Mapped[str] = mapped_column(TEXT, nullable=False)
