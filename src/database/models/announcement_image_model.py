import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column

from ..models.base_model import BaseModel


class AnnouncementImage(BaseModel):
    __tablename__ = 'announcement_image'

    announcement_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('announcement.id'), nullable=False, primary_key=True
    )
    image_url: Mapped[str] = mapped_column(TEXT, nullable=False)
