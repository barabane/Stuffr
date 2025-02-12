import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column

from ..models.base_model import BaseModel, CreatedAtMixin, IdPkUUIDMixin


class Review(BaseModel, IdPkUUIDMixin, CreatedAtMixin):
    __tablename__ = 'review'

    text: Mapped[str] = mapped_column(TEXT, nullable=True)
    user_to_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user.id'), nullable=False)
    user_from_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('user.id'), nullable=False
    )
