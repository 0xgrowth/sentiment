"""
app/__init__.py
---------------
Crypto Sentiment Tracker — main application package.

Sub-packages
------------
routers/    FastAPI route handlers (markets, analysis, alerts)
models/     SQLAlchemy ORM model definitions
schemas/    Pydantic request / response schemas
services/   Business logic & external integrations (Claude, yfinance)
utils/      Shared helpers (logging, formatting, datetime, crypto)
"""

__version__ = "0.1.0"
__author__  = "Crypto Sentiment Tracker"
