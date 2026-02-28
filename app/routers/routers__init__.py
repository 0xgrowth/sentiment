"""
app/routers/__init__.py
-----------------------
Router registry for the Crypto Sentiment Tracker API.

Import the shared `all_routers` list in main.py to register every
router in one place without touching main.py each time a new router
is added.

Usage in main.py:
    from app.routers import all_routers
    for router in all_routers:
        app.include_router(router)
"""

from app.routers.markets_router  import router as markets_router
from app.routers.analysis_router import router as analysis_router
from app.routers.alerts_router   import router as alerts_router

all_routers = [
    markets_router,
    analysis_router,
    alerts_router,
]

__all__ = [
    "markets_router",
    "analysis_router",
    "alerts_router",
    "all_routers",
]
