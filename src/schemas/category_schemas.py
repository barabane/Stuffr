from pydantic import BaseModel, Field


class GetCategoryScheme(BaseModel):
    id: int
    title: str = Field(min_length=3, max_length=100)


class CreateCategoryScheme(BaseModel):
    title: str = Field(min_length=3, max_length=100)


class UpdateCategoryScheme(CreateCategoryScheme):
    pass
