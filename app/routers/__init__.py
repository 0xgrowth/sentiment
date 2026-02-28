"""
app/routers/__init__.py
-----------------------
Registers all FastAPI routers. Import `all_routers` in main.py:

    from app.routers import all_routers
    for router in all_routers:
        app.include_router(router)
"""

from app.routers.markets_router  import router as markets_router   # noqa: F401
from app.routers.analysis_router import router as analysis_router  # noqa: F401
from app.routers.alerts_router   import router as alerts_router    # noqa: F401

all_routers = [
    markets_router,
    analysis_router,
    alerts_router,
]

__all__ = ["markets_router", "analysis_router", "alerts_router", "all_routers"]
