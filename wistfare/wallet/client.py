"""Wallet API client — balances, transfers, deposits & withdrawals."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from wistfare.client import Wistfare


class WalletClient:
    """Wallet API — balances, transfers, deposits, withdrawals & wallet members."""

    def __init__(self, client: Wistfare) -> None:
        self._client = client

    # ── Wallets ──

    def create(self, *, user_id: str, wallet_type: str, currency: str = "RWF") -> dict[str, Any]:
        """Create a new wallet."""
        return self._client.post("/v1/wallets", user_id=user_id, wallet_type=wallet_type, currency=currency)

    def get(self, wallet_id: str) -> dict[str, Any]:
        """Get a wallet by ID."""
        return self._client.get(f"/v1/wallets/{wallet_id}")

    def get_by_owner(self, user_id: str) -> dict[str, Any]:
        """Get a wallet by owner user ID."""
        return self._client.get("/v1/wallets/by-owner", user_id=user_id)

    def get_balance(self, wallet_id: str) -> dict[str, Any]:
        """Get wallet balance."""
        return self._client.get(f"/v1/wallets/{wallet_id}/balance")

    # ── Transfers ──

    def transfer(
        self,
        *,
        from_wallet_id: str,
        to_wallet_id: str,
        amount: str,
        idempotency_key: str,
        description: str | None = None,
    ) -> dict[str, Any]:
        """Transfer funds between wallets."""
        return self._client.post(
            "/v1/wallets/transfers",
            from_wallet_id=from_wallet_id,
            to_wallet_id=to_wallet_id,
            amount=amount,
            idempotency_key=idempotency_key,
            description=description,
        )

    def list_transactions(self, wallet_id: str, **pagination: Any) -> dict[str, Any]:
        """Get transaction history for a wallet."""
        return self._client.get(f"/v1/wallets/{wallet_id}/transactions", **pagination)

    # ── Deposits & Withdrawals ──

    def initiate_deposit(
        self,
        *,
        wallet_id: str,
        amount: str,
        payment_method: str,
        phone_number: str,
        currency: str = "RWF",
    ) -> dict[str, Any]:
        """Initiate a deposit (fund wallet via mobile money)."""
        return self._client.post(
            "/v1/wallets/deposits",
            wallet_id=wallet_id,
            amount=amount,
            payment_method=payment_method,
            phone_number=phone_number,
            currency=currency,
        )

    def initiate_withdrawal(
        self,
        *,
        wallet_id: str,
        amount: str,
        destination_type: str,
        destination_ref: str,
        currency: str = "RWF",
    ) -> dict[str, Any]:
        """Initiate a withdrawal (cash out to mobile money)."""
        return self._client.post(
            "/v1/wallets/withdrawals",
            wallet_id=wallet_id,
            amount=amount,
            destination_type=destination_type,
            destination_ref=destination_ref,
            currency=currency,
        )

    # ── Wallet Roles ──

    def create_role(self, *, wallet_id: str, name: str, permissions: list[str]) -> dict[str, Any]:
        """Create a role for a shared wallet."""
        return self._client.post("/v1/wallets/roles", wallet_id=wallet_id, name=name, permissions=permissions)

    def list_roles(self, wallet_id: str) -> dict[str, Any]:
        """List roles for a wallet."""
        return self._client.get(f"/v1/wallets/{wallet_id}/roles")

    def update_role(self, role_id: str, **params: Any) -> dict[str, Any]:
        """Update a wallet role."""
        return self._client.patch(f"/v1/wallets/roles/{role_id}", **params)

    def delete_role(self, role_id: str) -> None:
        """Delete a wallet role."""
        self._client.delete(f"/v1/wallets/roles/{role_id}")

    # ── Wallet Members ──

    def add_member(self, *, wallet_id: str, user_id: str, role_id: str) -> dict[str, Any]:
        """Add a member to a shared wallet."""
        return self._client.post("/v1/wallets/members", wallet_id=wallet_id, user_id=user_id, role_id=role_id)

    def list_members(self, wallet_id: str) -> dict[str, Any]:
        """List members of a wallet."""
        return self._client.get(f"/v1/wallets/{wallet_id}/members")

    def update_member_role(self, member_id: str, role_id: str) -> dict[str, Any]:
        """Update a member's role."""
        return self._client.patch(f"/v1/wallets/members/{member_id}", role_id=role_id)

    def remove_member(self, member_id: str) -> None:
        """Remove a member from a wallet."""
        self._client.delete(f"/v1/wallets/members/{member_id}")
