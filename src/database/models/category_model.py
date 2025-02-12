from sqlalchemy.dialects.postgresql import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from ..models.base_model import BaseModel, IdPkIntegerMixin


class Category(BaseModel, IdPkIntegerMixin):
    __tablename__ = 'category'

    title: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
