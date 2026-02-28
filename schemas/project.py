from uuid import UUID
from typing import List
from .base import ORMModel, TimestampSchema


class ProjectCreate(ORMModel):
    name: str
    owner_id: UUID
    organization_id: UUID


class ProjectUpdate(ORMModel):
    name: str | None = None


class ProjectResponse(TimestampSchema):
    name: str
    owner_id: UUID
    organization_id: UUID


## With nested tasks


from .task import TaskResponse


class ProjectDetail(ProjectResponse):
    tasks: List[TaskResponse] = []