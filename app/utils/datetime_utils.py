"""
app/utils/datetime_utils.py
----------------------------
UTC-aware datetime helpers used throughout the application.
All datetimes stored in the DB are UTC-naive (SQLite compat);
these helpers ensure consistent handling.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone


def utcnow() -> datetime:
    """Return current UTC time as a timezone-naive datetime (DB-safe)."""
    return datetime.utcnow()


def utcnow_aware() -> datetime:
    """Return current UTC time as a timezone-aware datetime."""
    return datetime.now(tz=timezone.utc)


def floor_to_hour(dt: datetime) -> datetime:
    """Truncate a datetime to the start of its hour — used for aggregate buckets."""
    return dt.replace(minute=0, second=0, microsecond=0)


def floor_to_minute(dt: datetime, interval: int = 5) -> datetime:
    """Truncate a datetime to the nearest N-minute boundary."""
    floored = dt.minute - (dt.minute % interval)
    return dt.replace(minute=floored, second=0, microsecond=0)


def iso_fmt(dt: datetime | None) -> str | None:
    """Return ISO-8601 string for a datetime, or None if dt is None."""
    return dt.isoformat() + "Z" if dt else None


def is_stale(dt: datetime | None, ttl_minutes: int) -> bool:
    """Return True if dt is None or older than ttl_minutes ago."""
    if dt is None:
        return True
    return (utcnow() - dt) > timedelta(minutes=ttl_minutes)


def minutes_ago(n: int) -> datetime:
    """Return UTC datetime n minutes in the past."""
    return utcnow() - timedelta(minutes=n)


def hours_ago(n: int) -> datetime:
    """Return UTC datetime n hours in the past."""
    return utcnow() - timedelta(hours=n)
