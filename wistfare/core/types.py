"""Shared types for the Wistfare SDK."""

from __future__ import annotations

from typing import TypedDict


class ListResponse(TypedDict):
    """Paginated list response."""

    data: list
    total: int
    page: int
    per_page: int
    has_more: bool


class PaginationParams(TypedDict, total=False):
    """Pagination query parameters."""

    page: int
    per_page: int


class Address(TypedDict, total=False):
    """Physical address."""

    city: str
    street: str
    district: str
    country: str
    latitude: float
    longitude: float


class ContactInfo(TypedDict, total=False):
    """Contact information."""

    phone: str
    email: str
    website: str
