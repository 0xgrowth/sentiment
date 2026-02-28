"""
app/utils/__init__.py
---------------------
Shared stateless utilities used across routers, services, and tests.

Modules
-------
crypto          Ticker normalisation, symbol validation, CRYPTO_TICKER_MAP
datetime_utils  UTC helpers, bucket rounding, ISO-8601 formatting
formatting      Price / score / percentage display formatters
logging         Structured JSON logger factory
"""

from app.utils.crypto         import normalise_symbol, is_valid_symbol, yf_symbol  # noqa: F401
from app.utils.datetime_utils import utcnow, floor_to_hour, iso_fmt                 # noqa: F401
from app.utils.formatting     import fmt_price, fmt_score, fmt_pct, fmt_confidence  # noqa: F401
from app.utils.logging        import get_logger                                      # noqa: F401

__all__ = [
    # crypto
    "normalise_symbol",
    "is_valid_symbol",
    "yf_symbol",
    # datetime
    "utcnow",
    "floor_to_hour",
    "iso_fmt",
    # formatting
    "fmt_price",
    "fmt_score",
    "fmt_pct",
    "fmt_confidence",
    # logging
    "get_logger",
]
