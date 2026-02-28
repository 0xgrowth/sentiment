import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, UUIDMixin, TimestampMixin


class Project(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(255))

    owner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id")
    )

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id")
    )

    owner = relationship("User", back_populates="projects")
    organization = relationship("Organization", back_populates="projects")
    tasks = relationship("Task", back_populates="project")