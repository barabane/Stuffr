from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, computed_field

from src.schemas.base_schemas import BaseSchemas
from src.schemas.common import OffsetLimitParams, StringUUIDField


class AnnouncementStatus(Enum):
    UNDER_REVIEW = 'UNDER_REVIEW'
    DECLINE = 'DECLINE'
    PUBLISHED = 'PUBLISHED'
    CLOSED = 'CLOSED'
    ARCHIVED = 'ARCHIVED'


class SearchParams(OffsetLimitParams):
    price_min: Optional[int] = None
    price_max: Optional[int] = None
    sort_by: Optional[str] = 'updated_at'
    category_id: Optional[int] = None


class SearchParamsProfile(OffsetLimitParams):
    pass


class GetAnnouncementScheme(BaseModel):
    id: StringUUIDField
    title: str = Field(min_length=3, max_length=100)
    description: str
    price: Optional[int] = None
    price_with_discount: Optional[int] = None
    discount: Optional[int] = Field(default=None, ge=1, le=99)
    currency: Optional[str] = Field(min_length=3, max_length=3, default='RUB')
    user_id: StringUUIDField


class GetMyAnnouncementScheme(GetAnnouncementScheme):
    status: Optional[str] = Field(max_length=15)


class CreateAnnouncementOuterScheme(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str
    price: Optional[int] = None
    discount: Optional[int] = Field(default=None, ge=1, le=99)
    currency: Optional[str] = Field(min_length=3, max_length=3, default='RUB')
    category_id: int = Field(ge=1)

    @computed_field
    @property
    def price_with_discount(self) -> int:
        if not self.discount:
            return None
        return round(self.price - round((self.price * self.discount) / 100))


class CreateAnnouncementScheme(CreateAnnouncementOuterScheme):
    user_id: StringUUIDField


class UpdateAnnouncementOuterScheme(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str
    price: Optional[int] = None
    discount: Optional[int] = Field(default=None, ge=1, le=99)
    currency: Optional[str] = Field(min_length=3, max_length=3, default='RUB')
    category_id: int = Field(ge=1)

    @computed_field
    @property
    def price_with_discount(self) -> int:
        if not self.discount:
            return None
        return round(self.price - round((self.price * self.discount) / 100))


class UpdateAnnouncementScheme(UpdateAnnouncementOuterScheme):
    status: Optional[str] = Field(
        max_length=15, default=AnnouncementStatus.UNDER_REVIEW.value
    )


class AnnouncementSchemas(BaseSchemas):
    def __init__(
        self, get_scheme: BaseModel, create_scheme: BaseModel, update_scheme: BaseModel
    ):
        self.get_scheme = get_scheme
        self.create_scheme = create_scheme
        self.update_scheme = update_scheme


def get_announcement_schemas() -> AnnouncementSchemas:
    return AnnouncementSchemas(
        get_scheme=GetAnnouncementScheme,
        create_scheme=CreateAnnouncementScheme,
        update_scheme=UpdateAnnouncementScheme,
    )
