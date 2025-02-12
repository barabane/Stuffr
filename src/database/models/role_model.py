from sqlalchemy.dialects.postgresql import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from ..models.base_model import BaseModel, IdPkIntegerMixin


class Role(BaseModel, IdPkIntegerMixin):
    __tablename__ = 'role'

    name: Mapped[str] = mapped_column(VARCHAR(30), nullable=False)
