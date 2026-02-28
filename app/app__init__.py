"""
app/__init__.py
---------------
Crypto Sentiment Tracker — backend application package.

Package layout:
  app/
  ├── __init__.py          ← you are here
  ├── main.py              ← FastAPI app + lifespan
  ├── config.py            ← Settings (reads .env via pydantic-settings)
  ├── database.py          ← Shared async engine + session factory
  ├── scheduler.py         ← Shared APScheduler instance
  └── routers/
      ├── __init__.py
      ├── markets_router.py
      ├── analysis_router.py
      └── alerts_router.py
"""

__version__ = "0.1.0"
__author__  = "Crypto Sentiment Tracker"
