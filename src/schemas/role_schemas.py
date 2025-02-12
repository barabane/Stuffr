from pydantic import BaseModel, Field


class GetRoleScheme(BaseModel):
    id: int
    name: str = Field(min_length=3, max_length=30)


class CreateRoleScheme(BaseModel):
    name: str = Field(min_length=3, max_length=30)


class UpdateRoleScheme(CreateRoleScheme):
    pass
