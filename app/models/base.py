"""
app/models/base.py
------------------
Shared SQLAlchemy declarative base.
Import Base here — never create a second one.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Project-wide SQLAlchemy declarative base."""
    pass
