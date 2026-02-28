"""
app/utils/formatting.py
------------------------
Display formatters for prices, sentiment scores, percentages, and
confidence values. Used in Claude prompts, log messages, and API
response construction to ensure consistent representation across the app.
"""

from __future__ import annotations


def fmt_price(value: float | None, decimals: int = 4) -> str:
    """
    Format a price as a USD string.
    fmt_price(70123.456)  → "$70,123.4560"
    fmt_price(None)       → "N/A"
    """
    if value is None:
        return "N/A"
    return f"${value:,.{decimals}f}"


def fmt_score(value: float | None) -> str:
    """
    Format a sentiment / impact score (–1 … +1) as a signed percentage.
    fmt_score(0.735)   → "+73.5%"
    fmt_score(-0.42)   → "-42.0%"
    fmt_score(None)    → "—"
    """
    if value is None:
        return "—"
    sign = "+" if value >= 0 else ""
    return f"{sign}{value * 100:.1f}%"


def fmt_pct(value: float | None, decimals: int = 2) -> str:
    """
    Format a raw percentage value (e.g. 24h change).
    fmt_pct(3.14)   → "+3.14%"
    fmt_pct(-1.5)   → "-1.50%"
    fmt_pct(None)   → "—"
    """
    if value is None:
        return "—"
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.{decimals}f}%"


def fmt_confidence(value: float | None) -> str:
    """
    Format a confidence score (0 … 1) as a percentage.
    fmt_confidence(0.87) → "87%"
    fmt_confidence(None) → "—"
    """
    if value is None:
        return "—"
    return f"{value * 100:.0f}%"


def fmt_volume(value: float | None) -> str:
    """
    Human-readable volume with magnitude suffix.
    fmt_volume(1_234_567) → "1.23M"
    fmt_volume(None)      → "N/A"
    """
    if value is None:
        return "N/A"
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if value >= 1_000:
        return f"{value / 1_000:.2f}K"
    return f"{value:.0f}"
