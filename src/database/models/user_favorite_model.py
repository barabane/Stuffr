import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..models.base_model import BaseModel, IdPkIntegerMixin


class UserFavorite(BaseModel, IdPkIntegerMixin):
    __tablename__ = 'user_favorite'

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('user.id'), nullable=False, index=True
    )
    announcement_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('announcement.id'), nullable=False
    )
