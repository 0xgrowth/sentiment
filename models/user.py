import uuid
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, UUIDMixin, TimestampMixin


class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    organization_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=True,
    )

    organization = relationship("Organization", back_populates="users")
    roles = relationship("Role", secondary="user_roles", back_populates="users")
    projects = relationship("Project", back_populates="owner")