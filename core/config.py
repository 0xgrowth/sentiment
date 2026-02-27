from functools import lru_cache
from typing import List, Optional

from pydantic import Field, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # -----------------------------------------------------------------------------
    # App
    # -----------------------------------------------------------------------------
    app_name: str = "AI Market Tracker"
    app_version: str = "1.0.0"
    environment: str = Field(default="development", pattern="^(development|staging|production)$")
    debug: bool = False

    # -----------------------------------------------------------------------------
    # API
    # -----------------------------------------------------------------------------
    api_prefix: str = "/api/v1"
    allowed_origins: List[str] = ["*"]

    # -----------------------------------------------------------------------------
    # Security
    # -----------------------------------------------------------------------------
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60

    # -----------------------------------------------------------------------------
    # Database
    # -----------------------------------------------------------------------------
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/market"

    # -----------------------------------------------------------------------------
    # Redis / Cache
    # -----------------------------------------------------------------------------
    redis_url: Optional[str] = None

    # -----------------------------------------------------------------------------
    # External Market APIs
    # -----------------------------------------------------------------------------
    binance_api_key: Optional[str] = None
    binance_api_secret: Optional[str] = None
    alpaca_api_key: Optional[str] = None
    alpaca_api_secret: Optional[str] = None

    # -----------------------------------------------------------------------------
    # AI Model
    # -----------------------------------------------------------------------------
    model_path: str = "models/latest.pt"
    model_confidence_threshold: float = 0.75

    # -----------------------------------------------------------------------------
    # Observability
    # -----------------------------------------------------------------------------
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


# Cached singleton (important for FastAPI performance)
@lru_cache
def get_settings() -> Settings:
    return Settings()