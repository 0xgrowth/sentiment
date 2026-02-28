"""
app/schemas/__init__.py
-----------------------
Pydantic v2 request / response schemas (API contract layer).
Schemas are kept separate from ORM models to decouple
the DB layer from the API surface.
"""

from app.schemas.market   import MarketSnapshotOut        # noqa: F401
from app.schemas.sentiment import (                       # noqa: F401
    SentimentRecordOut,
    AnalyseSentimentRequest,
    SentimentResult,
)
from app.schemas.ai_impact import (                       # noqa: F401
    AIImpactRecordOut,
    AnalyseImpactRequest,
)
from app.schemas.alert import (                           # noqa: F401
    AlertRuleOut,
    AlertEventOut,
    CreateAlertRuleRequest,
    UpdateAlertRuleRequest,
    AcknowledgeRequest,
    AlertSummaryOut,
)

__all__ = [
    "MarketSnapshotOut",
    "SentimentRecordOut",
    "AnalyseSentimentRequest",
    "SentimentResult",
    "AIImpactRecordOut",
    "AnalyseImpactRequest",
    "AlertRuleOut",
    "AlertEventOut",
    "CreateAlertRuleRequest",
    "UpdateAlertRuleRequest",
    "AcknowledgeRequest",
    "AlertSummaryOut",
]
