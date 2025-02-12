import uuid
from typing import Optional

from pydantic import BaseModel


class GetReviewScheme(BaseModel):
    id: str | uuid.UUID
    text: Optional[str] = None
    user_to_id: str | uuid.UUID
    user_from_id: str | uuid.UUID


class CreateReviewScheme(BaseModel):
    text: Optional[str] = None
    user_to_id: str | uuid.UUID
    user_from_id: str | uuid.UUID


class UpdateReviewScheme(BaseModel):
    text: Optional[str] = None
