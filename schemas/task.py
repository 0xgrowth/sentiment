from uuid import UUID
from .base import ORMModel, TimestampSchemaf


class TaskCreate(ORMModel):
    title: str
    description: str | None = None
    project_id: UUID
    assignee_id: UUID | None = None


class TaskUpdate(ORMModel):
    title: str | None = None
    description: str | None = None
    assignee_id: UUID | None = None


class TaskResponse(TimestampSchema):
    title: str
    description: str | None
    project_id: UUID
    assignee_id: UUID | None