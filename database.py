from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from app.core.config import settings  # adjust to your project


# -------------------------------------------------------------------
# Base Model
# -------------------------------------------------------------------

class Base(DeclarativeBase):
    pass


# -------------------------------------------------------------------
# Async Engine
# -------------------------------------------------------------------

engine = create_async_engine(
    settings.DATABASE_URL,  # e.g. "postgresql+asyncpg://user:pass@localhost/db"
    echo=False,              # Set True for SQL debugging
    pool_pre_ping=True,      # Avoid stale connections
    poolclass=NullPool if settings.DEBUG else None,
)


# -------------------------------------------------------------------
# Async Session Factory
# -------------------------------------------------------------------

AsyncSessionFactory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# -------------------------------------------------------------------
# Dependency (FastAPI-ready)
# -------------------------------------------------------------------

async def get_db() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        try:
            yield session
        finally:
            await session.close()