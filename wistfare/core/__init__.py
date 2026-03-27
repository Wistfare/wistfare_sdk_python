"""Wistfare Core — HTTP client, authentication, errors, and shared types."""

from wistfare.core.client import Wistfare
from wistfare.core.errors import (
    WistfareError,
    AuthenticationError,
    PermissionError,
    NotFoundError,
    ValidationError,
    RateLimitError,
)
from wistfare.core.types import (
    ListResponse,
    PaginationParams,
    Address,
    ContactInfo,
)

__all__ = [
    "Wistfare",
    "WistfareError",
    "AuthenticationError",
    "PermissionError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
    "ListResponse",
    "PaginationParams",
    "Address",
    "ContactInfo",
]
