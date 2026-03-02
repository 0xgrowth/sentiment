from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from app.core.config import settings


# -------------------------------------------------------------------
# Base Model
# -------------------------------------------------------------------

class Base(DeclarativeBase):
    pass


# -------------------------------------------------------------------
# Async Engine
# -------------------------------------------------------------------

engine_kwargs = {
    "echo": settings.DEBUG,
    "pool_pre_ping": True,
}

if settings.DEBUG:
    engine_kwargs["poolclass"] = NullPool

engine = create_async_engine(
    settings.DATABASE_URL,
    **engine_kwargs,
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
# Dependency
# -------------------------------------------------------------------

async def get_db() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session