from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, FLOAT, TEXT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.role_model import Role  # noqa

from ..models.base_model import BaseModel, IdPkUUIDMixin, MutableList


class User(BaseModel, IdPkUUIDMixin):
    __tablename__ = 'user'

    name: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
    second_name: Mapped[str] = mapped_column(VARCHAR(30), nullable=True)
    avatar_url: Mapped[str] = mapped_column(TEXT, nullable=True)
    role_id: Mapped[int] = mapped_column(
        ForeignKey('role.id'), nullable=False, default=1
    )
    rating: Mapped[float] = mapped_column(FLOAT, nullable=True)
    phone: Mapped[str] = mapped_column(VARCHAR(20), nullable=True)
    email: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    hashed_password: Mapped[str] = mapped_column(TEXT, nullable=False)
    refresh_tokens: Mapped[List[str]] = mapped_column(
        MutableList.as_mutable(ARRAY(TEXT)), nullable=False, default=[]
    )
