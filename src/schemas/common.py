from pydantic import BaseModel


class OffsetLimitParams(BaseModel):
    offset: int = 0
    limit: int = 10
