"""
app/models/__init__.py
----------------------
SQLAlchemy ORM model registry.

All models are imported here so that:
  • Alembic autogenerate can discover every table in one import.
  • `Base.metadata.create_all()` in tests creates all tables.

Add new models to this file as the schema grows.
"""

from app.models.base import Base                          # noqa: F401
from app.models.market   import MarketSnapshot            # noqa: F401
from app.models.watchlist import WatchlistEntry           # noqa: F401
from app.models.sentiment import SentimentRecord          # noqa: F401
from app.models.ai_impact import AIImpactRecord           # noqa: F401
from app.models.aggregate import SentimentAggregate       # noqa: F401
from app.models.alert     import AlertRule, AlertEvent    # noqa: F401

__all__ = [
    "Base",
    "MarketSnapshot",
    "WatchlistEntry",
    "SentimentRecord",
    "AIImpactRecord",
    "SentimentAggregate",
    "AlertRule",
    "AlertEvent",
]
