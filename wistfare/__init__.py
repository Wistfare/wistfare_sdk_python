"""Wistfare Python SDK."""

from wistfare.client import Wistfare
from wistfare.errors import (
    WistfareError,
    AuthenticationError,
    PermissionError as WistfarePermissionError,
    NotFoundError,
    ValidationError,
    RateLimitError,
)

__version__ = "0.1.0"
__all__ = [
    "Wistfare",
    "WistfareError",
    "AuthenticationError",
    "WistfarePermissionError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
]
