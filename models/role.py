from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, UUIDMixin


class Role(Base, UUIDMixin):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(100), unique=True)

    users = relationship("User", secondary="user_roles", back_populates="roles")