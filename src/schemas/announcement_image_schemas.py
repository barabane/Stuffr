import uuid

from pydantic import BaseModel, HttpUrl


class GetAnnouncementImage(BaseModel):
    announcement_id: str | uuid.UUID
    image_url: HttpUrl


class CreateAnnouncementImage(BaseModel):
    image_url: HttpUrl


class UpdateAnnouncementImage(CreateAnnouncementImage):
    pass
