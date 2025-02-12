import datetime

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP, UUID
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.orm import Mapped, as_declarative, declared_attr, mapped_column
from uuid_extensions import uuid7


@as_declarative()
class BaseModel:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class IdPkUUIDMixin:
    id: Mapped[str] = mapped_column(UUID, default=uuid7, primary_key=True, index=True)


class IdPkIntegerMixin:
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, index=True)


class CreatedAtMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )


class UpdatedAtMixin:
    updated_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )


class MutableList(Mutable, list):
    def append(self, value):
        super().append(value)
        self.changed()

    def pop(self, index=0):
        value = super().pop(index)
        self.changed()
        return value

    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, index, value):
        super().__setitem__(index, value)
        self.changed()

    def __delitem__(self, index):
        super().__delitem__(index)
        self.changed()

    def extend(self, iterable):
        super().extend(iterable)
        self.changed()

    def insert(self, index, value):
        super().insert(index, value)
        self.changed()

    def remove(self, value):
        super().remove(value)
        self.changed()
