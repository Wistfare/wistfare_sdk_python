"""Backward-compatible top-level Wistfare error exports."""

from wistfare.core.errors import (
    AuthenticationError,
    NotFoundError,
    PermissionError,
    RateLimitError,
    ValidationError,
    WistfareError,
)

__all__ = [
    "AuthenticationError",
    "NotFoundError",
    "PermissionError",
    "RateLimitError",
    "ValidationError",
    "WistfareError",
]
