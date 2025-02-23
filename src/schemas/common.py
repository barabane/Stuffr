from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, BeforeValidator


class OffsetLimitParams(BaseModel):
    offset: int = 0
    limit: int = 10


def uuid_to_str(value: UUID):
    return str(value)


StringUUIDField = Annotated[str | UUID, BeforeValidator(uuid_to_str)]
