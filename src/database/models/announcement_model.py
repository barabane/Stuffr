import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import INTEGER, TEXT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.category_model import Category  # noqa

from ...schemas.announcement_schemas import AnnouncementStatus
from ..models.base_model import BaseModel, CreatedAtMixin, IdPkUUIDMixin, UpdatedAtMixin


class Announcement(BaseModel, IdPkUUIDMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = 'announcement'

    title: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    description: Mapped[str] = mapped_column(TEXT, nullable=False)
    price: Mapped[int] = mapped_column(INTEGER, nullable=True)
    price_with_discount: Mapped[int] = mapped_column(INTEGER, nullable=True)
    discount: Mapped[int] = mapped_column(nullable=True)
    currency: Mapped[str] = mapped_column(VARCHAR(3), nullable=False, default='RUB')
    status: Mapped[str] = mapped_column(
        VARCHAR(15), nullable=False, default=AnnouncementStatus.UNDER_REVIEW.value
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user.id'), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'), nullable=False)
