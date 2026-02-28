"""
app/utils/crypto.py
-------------------
Ticker normalisation, symbol validation, and yfinance symbol mapping.

Single source of truth for the CRYPTO_TICKER_MAP so every router and
service references the same mapping rather than maintaining duplicates.
"""

from __future__ import annotations

CRYPTO_TICKER_MAP: dict[str, str] = {
    "BTC":   "BTC-USD",
    "ETH":   "ETH-USD",
    "SOL":   "SOL-USD",
    "BNB":   "BNB-USD",
    "XRP":   "XRP-USD",
    "ADA":   "ADA-USD",
    "DOGE":  "DOGE-USD",
    "AVAX":  "AVAX-USD",
    "DOT":   "DOT-USD",
    "MATIC": "MATIC-USD",
    "LINK":  "LINK-USD",
    "UNI":   "UNI-USD",
    "ATOM":  "ATOM-USD",
    "LTC":   "LTC-USD",
}

SUPPORTED_SYMBOLS: frozenset[str] = frozenset(CRYPTO_TICKER_MAP.keys())


def normalise_symbol(symbol: str) -> str:
    """Return uppercase symbol, e.g. "btc" → "BTC"."""
    return symbol.strip().upper()


def is_valid_symbol(symbol: str) -> bool:
    """Return True if symbol is in the supported set."""
    return normalise_symbol(symbol) in SUPPORTED_SYMBOLS


def yf_symbol(symbol: str) -> str:
    """
    Return the yfinance ticker string for a given symbol.

    Falls back to "<SYMBOL>-USD" for unlisted symbols so callers
    can still attempt a lookup without crashing.

    Example:
        yf_symbol("BTC")  → "BTC-USD"
        yf_symbol("PEPE") → "PEPE-USD"  (fallback)
    """
    upper = normalise_symbol(symbol)
    return CRYPTO_TICKER_MAP.get(upper, f"{upper}-USD")
