from uuid import UUID
from pydantic import EmailStr, Field
from .base import ORMModel, TimestampSchema


class UserCreate(ORMModel):
    email: EmailStr
    password: str = Field(min_length=8)
    organization_id: UUID | None = None


## Update


class UserUpdate(ORMModel):
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8)
    is_active: bool | None = None


## Response


class UserResponse(TimestampSchema):
    email: EmailStr
    is_active: bool
    organization_id: UUID | None


## Detailed (with relationships)


from typing import List
from .role import RoleResponse


class UserDetail(UserResponse):
    roles: List[RoleResponse] = []




# 🏢 `schemas/organization.py`


from .base import ORMModel, TimestampSchema


class OrganizationCreate(ORMModel):
    name: str


class OrganizationUpdate(ORMModel):
    name: str | None = None


class OrganizationResponse(TimestampSchema):
    name: str