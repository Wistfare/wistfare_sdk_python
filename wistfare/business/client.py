"""Business API client."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from wistfare.core.client import Wistfare


class BusinessClient:
    """Business API — retrieve and list businesses."""

    def __init__(self, client: Wistfare) -> None:
        self._client = client

    def get(self, business_id: str) -> dict[str, Any]:
        """Get a business by ID."""
        return self._client.get(f"/v1/businesses/{business_id}")

    def list(
        self,
        *,
        business_id: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> dict[str, Any]:
        """List businesses, optionally filtered by business ID."""
        params: dict[str, Any] = {}
        if business_id is not None:
            params["business_id"] = business_id
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        return self._client.get("/v1/businesses", **params)
