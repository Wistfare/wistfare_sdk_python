"""Wallet API client — get wallets and transfer funds."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from wistfare.core.client import Wistfare


class WalletClient:
    """Wallet API — get wallets and transfer funds."""

    def __init__(self, client: Wistfare) -> None:
        self._client = client

    def get(
        self,
        *,
        wallet_id: str | None = None,
        owner_id: str | None = None,
    ) -> dict[str, Any]:
        """Get a wallet by wallet ID or owner ID (query params)."""
        params: dict[str, Any] = {}
        if wallet_id is not None:
            params["wallet_id"] = wallet_id
        if owner_id is not None:
            params["owner_id"] = owner_id
        return self._client.get("/v1/wallets", **params)

    def transfer(
        self,
        *,
        from_wallet_id: str,
        to_wallet_id: str,
        amount: str,
        reference_id: str,
        description: str | None = None,
    ) -> dict[str, Any]:
        """Transfer funds between wallets."""
        return self._client.post(
            "/v1/wallets/transfers",
            from_wallet_id=from_wallet_id,
            to_wallet_id=to_wallet_id,
            amount=amount,
            reference_id=reference_id,
            description=description,
        )
