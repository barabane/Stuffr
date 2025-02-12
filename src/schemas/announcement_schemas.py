import uuid
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


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
    status: Optional[AnnouncementStatus] = Field(
        max_length=15, default=AnnouncementStatus.UNDER_REVIEW
    )
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
