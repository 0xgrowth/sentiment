"""
app/config.py
-------------
Centralised settings for the Crypto Sentiment Tracker backend.
All values are read from environment variables / .env file via
pydantic-settings. Import the `settings` singleton anywhere in the app.

Usage:
    from app.config import settings
    print(settings.anthropic_api_key)
"""

from functools import lru_cache
from typing import List, Literal, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    All configurable values for the application.
    Override any value by setting the corresponding environment variable
    or adding it to your .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ────────────────────────────────────────────────────────
    app_name:    str  = "Crypto Sentiment Tracker"
    app_version: str  = "0.1.0"
    environment: Literal["development", "staging", "production"] = "development"
    debug:       bool = False
    log_level:   str  = "INFO"

    # ── API Server ─────────────────────────────────────────────────────────
    host:              str = "0.0.0.0"
    port:              int = 8000
    workers:           int = 1
    reload:            bool = True   # set False in production

    # ── CORS ───────────────────────────────────────────────────────────────
    cors_origins: List[str] = Field(
        default=["http://localhost:5173", "http://localhost:3000"],
        description="Allowed CORS origins (React dev server defaults)",
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_cors(cls, v):
        """Allow CORS_ORIGINS as a comma-separated string in .env."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # ── Database ───────────────────────────────────────────────────────────
    database_url: str = Field(
        default="sqlite+aiosqlite:///./crypto_sentiment.db",
        description=(
            "Async SQLAlchemy URL. "
            "SQLite for dev: sqlite+aiosqlite:///./crypto_sentiment.db "
            "Postgres for prod: postgresql+asyncpg://user:pass@host/db"
        ),
    )
    db_echo:       bool = False   # set True to log all SQL statements
    db_pool_size:  int  = 5
    db_max_overflow: int = 10

    # ── Anthropic / Claude ─────────────────────────────────────────────────
    anthropic_api_key: str = Field(
        ...,
        description="Your Anthropic API key (required). Get one at console.anthropic.com",
    )
    anthropic_model: str = Field(
        default="claude-sonnet-4-20250514",
        description="Claude model to use for sentiment and narrative generation",
    )
    anthropic_max_tokens: int = Field(
        default=1024,
        description="Max tokens for Claude responses",
    )
    anthropic_timeout: float = Field(
        default=30.0,
        description="HTTP timeout (seconds) for Anthropic API calls",
    )

    # ── yfinance / Market Data ─────────────────────────────────────────────
    market_cache_ttl_minutes: int = Field(
        default=5,
        description="How long a market snapshot is considered fresh before re-fetching",
    )
    default_symbols: List[str] = Field(
        default=["BTC", "ETH", "SOL", "BNB", "XRP"],
        description="Symbols refreshed on every scheduler tick",
    )

    @field_validator("default_symbols", mode="before")
    @classmethod
    def split_symbols(cls, v):
        if isinstance(v, str):
            return [s.strip().upper() for s in v.split(",")]
        return [s.upper() for s in v]

    # ── APScheduler ────────────────────────────────────────────────────────
    markets_refresh_interval_minutes:  int = Field(default=5,  description="Markets data refresh cadence")
    analysis_refresh_interval_minutes: int = Field(default=15, description="Sentiment analysis refresh cadence")
    alerts_eval_interval_minutes:      int = Field(default=5,  description="Alert rule evaluation cadence")
    scheduler_timezone:                str = "UTC"
    scheduler_misfire_grace_seconds:   int = 30

    # ── Security (future-proofing) ─────────────────────────────────────────
    secret_key: str = Field(
        default="change-me-in-production-use-a-long-random-string",
        description="Used for signing tokens / session cookies",
    )
    api_key_header: str = Field(
        default="X-API-Key",
        description="Header name for optional API key authentication",
    )
    internal_api_key: Optional[str] = Field(
        default=None,
        description="If set, all API requests must include this key in the X-API-Key header",
    )

    # ── Rate Limiting (optional — requires slowapi) ────────────────────────
    rate_limit_enabled:           bool = False
    rate_limit_per_minute:        int  = 60
    rate_limit_sentiment_per_hour: int = 100   # Claude calls are metered


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Return the cached Settings singleton.
    Use this as a FastAPI dependency or import `settings` directly.
    """
    return Settings()


# Convenient module-level singleton — import this directly in routers
settings = get_settings()
