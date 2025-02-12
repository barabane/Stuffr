import uuid
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from src.schemas.base_schemas import BaseSchemas


class AnnouncementStatus(Enum):
    UNDER_REVIEW = 'UNDER_REVIEW'
    UNDER_REVISION = 'UNDER_REVISION'
    PUBLISHED = 'PUBLISHED'
    CLOSED = 'CLOSED'


class GetAnnouncementScheme(BaseModel):
    id: str | uuid.UUID
    title: str = Field(min_length=3, max_length=100)
    description: str
    price: Optional[int] = None
    currency: Optional[str] = Field(min_length=3, max_length=3, default='RUB')
    status: Optional[AnnouncementStatus] = Field(
        max_length=15, default=AnnouncementStatus.UNDER_REVIEW
    )
    user_id: str | uuid.UUID
    category_id: int = Field(ge=1)


class CreateAnnouncementScheme(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str
    price: Optional[int] = None
    currency: Optional[str] = Field(min_length=3, max_length=3, default='RUB')
    user_id: str | uuid.UUID
    category_id: int = Field(ge=1)


class UpdateAnnouncementScheme(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str
    price: Optional[int] = None
    currency: Optional[str] = Field(min_length=3, max_length=3, default='RUB')
    status: Optional[AnnouncementStatus] = Field(
        max_length=15, default=AnnouncementStatus.UNDER_REVIEW
    )
    category_id: int = Field(ge=1)


class AnnouncementSchemas(BaseSchemas):
    def __init__(
        self, get_scheme: BaseModel, crate_scheme: BaseModel, update_scheme: BaseModel
    ):
        self.get_scheme = get_scheme
        self.crate_scheme = crate_scheme
        self.update_scheme = update_scheme


def get_announcement_schemas() -> AnnouncementSchemas:
    return AnnouncementSchemas(
        get_scheme=GetAnnouncementScheme,
        crate_scheme=CreateAnnouncementScheme,
        update_scheme=UpdateAnnouncementScheme,
    )
