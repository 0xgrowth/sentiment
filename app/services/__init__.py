"""
app/services/__init__.py
------------------------
Business logic and external integrations.

market_service    → yfinance data fetching + caching
sentiment_service → Claude sentiment analysis via Anthropic SDK
impact_service    → Claude AI-impact analysis
alert_service     → alert rule evaluation + event firing
scheduler_service → APScheduler setup and job registration
"""

from app.services.market_service    import fetch_market_data      # noqa: F401
from app.services.sentiment_service import analyse_sentiment      # noqa: F401
from app.services.impact_service    import analyse_ai_impact      # noqa: F401
from app.services.alert_service     import evaluate_all_rules     # noqa: F401
from app.services.scheduler_service import (                      # noqa: F401
    start_all_schedulers,
    stop_all_schedulers,
)

__all__ = [
    "fetch_market_data",
    "analyse_sentiment",
    "analyse_ai_impact",
    "evaluate_all_rules",
    "start_all_schedulers",
    "stop_all_schedulers",
]
