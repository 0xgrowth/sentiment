from .base import ORMModel, TimestampSchema


class RoleCreate(ORMModel):
    name: str


class RoleResponse(TimestampSchema):
    name: str