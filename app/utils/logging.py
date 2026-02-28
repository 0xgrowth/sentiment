"""
app/utils/logging.py
---------------------
Structured JSON logger factory.

Usage:
    from app.utils.logging import get_logger
    logger = get_logger(__name__)
    logger.info("Snapshot refreshed", extra={"symbol": "BTC", "price": 70123.45})

In development (LOG_LEVEL=DEBUG) logs are pretty-printed to stdout.
In production (LOG_LEVEL=INFO/WARNING) logs are emitted as JSON for
ingestion by log aggregators (Datadog, CloudWatch, Loki, etc.).
"""

from __future__ import annotations

import logging
import os
import sys


def get_logger(name: str) -> logging.Logger:
    """
    Return a named logger configured for the current environment.

    Reads LOG_LEVEL from the environment (default: INFO).
    If pythonjsonlogger is installed, production logs are JSON-formatted.
    Falls back to plain text if the package is not available.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        # Already configured — avoid adding duplicate handlers
        return logger

    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level     = getattr(logging, log_level_str, logging.INFO)
    logger.setLevel(log_level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    environment = os.getenv("ENVIRONMENT", "development")

    if environment == "production":
        try:
            from pythonjsonlogger import jsonlogger  # type: ignore[import]
            formatter = jsonlogger.JsonFormatter(
                fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S",
            )
        except ImportError:
            # Graceful fallback if python-json-logger is not installed
            formatter = logging.Formatter(
                fmt="%(asctime)s | %(name)-30s | %(levelname)-8s | %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S",
            )
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(name)-30s | %(levelname)-8s | %(message)s",
            datefmt="%H:%M:%S",
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False

    return logger
