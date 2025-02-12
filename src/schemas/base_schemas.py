from pydantic import BaseModel


class GetBaseScheme(BaseModel):
    pass


class CreateBaseScheme(BaseModel):
    pass


class UpdateBaseScheme(BaseModel):
    pass


class BaseSchemas:
    def __init__(
        self, get_scheme: BaseModel, crate_scheme: BaseModel, update_scheme: BaseModel
    ):
        self.get_scheme: BaseModel = get_scheme
        self.crate_scheme: BaseModel = crate_scheme
        self.update_scheme: BaseModel = update_scheme


def get_base_schemas() -> BaseSchemas:
    return BaseSchemas(
        get_scheme=GetBaseScheme,
        crate_scheme=CreateBaseScheme,
        update_scheme=UpdateBaseScheme,
    )
