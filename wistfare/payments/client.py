"""Payments API client — collections, disbursements, fees & payment requests."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from wistfare.client import Wistfare


class PaymentsClient:
    """Payments API — collections, disbursements, fee management & payment requests."""

    def __init__(self, client: Wistfare) -> None:
        self._client = client

    # ── Fee Management ──

    def set_fee_config(
        self,
        *,
        business_id: str,
        transaction_type: str,
        fee_model: str,
        percentage_rate: str | None = None,
        flat_amount: str | None = None,
        min_fee: str | None = None,
        max_fee: str | None = None,
        currency: str = "RWF",
    ) -> dict[str, Any]:
        """Configure fees for a business."""
        return self._client.post(
            "/v1/fees",
            business_id=business_id,
            transaction_type=transaction_type,
            fee_model=fee_model,
            percentage_rate=percentage_rate,
            flat_amount=flat_amount,
            min_fee=min_fee,
            max_fee=max_fee,
            currency=currency,
        )

    def get_fee_config(self, business_id: str, transaction_type: str) -> dict[str, Any]:
        """Get fee configuration for a business and transaction type."""
        return self._client.get(f"/v1/fees/{business_id}", transaction_type=transaction_type)

    def list_fee_configs(self, business_id: str, **pagination: Any) -> dict[str, Any]:
        """List all fee configs for a business."""
        return self._client.get("/v1/fees", business_id=business_id, **pagination)

    def delete_fee_config(self, fee_config_id: str) -> None:
        """Delete a fee config."""
        self._client.delete(f"/v1/fees/{fee_config_id}")

    def calculate_fee(
        self,
        *,
        business_id: str,
        amount: str,
        transaction_type: str,
        currency: str = "RWF",
    ) -> dict[str, Any]:
        """Calculate fee for a given amount."""
        return self._client.post(
            "/v1/fees/calculate",
            business_id=business_id,
            amount=amount,
            transaction_type=transaction_type,
            currency=currency,
        )

    # ── Payment Requests (QR / Links) ──

    def create_payment_request(
        self,
        *,
        business_id: str,
        wallet_id: str,
        request_type: str,
        amount: str,
        currency: str = "RWF",
        description: str | None = None,
        customer_phone: str | None = None,
        customer_name: str | None = None,
        max_uses: int | None = None,
        expires_at: str | None = None,
    ) -> dict[str, Any]:
        """Create a payment request (QR code or payment link)."""
        return self._client.post(
            "/v1/payment-requests",
            business_id=business_id,
            wallet_id=wallet_id,
            request_type=request_type,
            amount=amount,
            currency=currency,
            description=description,
            customer_phone=customer_phone,
            customer_name=customer_name,
            max_uses=max_uses,
            expires_at=expires_at,
        )

    def get_payment_request(self, request_id: str) -> dict[str, Any]:
        """Get a payment request by ID."""
        return self._client.get(f"/v1/payment-requests/{request_id}")

    def list_payment_requests(self, business_id: str, **pagination: Any) -> dict[str, Any]:
        """List payment requests for a business."""
        return self._client.get("/v1/payment-requests", business_id=business_id, **pagination)

    def cancel_payment_request(self, request_id: str) -> dict[str, Any]:
        """Cancel a payment request."""
        return self._client.post(f"/v1/payment-requests/{request_id}/cancel")

    # ── Collections ──

    def initiate_collection(
        self,
        *,
        business_id: str,
        wallet_id: str,
        customer_phone: str,
        amount: str,
        payment_method: str,
        currency: str = "RWF",
        description: str | None = None,
        external_id: str | None = None,
    ) -> dict[str, Any]:
        """Initiate a mobile money collection from a customer."""
        return self._client.post(
            "/v1/collections",
            business_id=business_id,
            wallet_id=wallet_id,
            customer_phone=customer_phone,
            amount=amount,
            payment_method=payment_method,
            currency=currency,
            description=description,
            external_id=external_id,
        )

    # ── Transactions ──

    def get_transaction(self, transaction_id: str) -> dict[str, Any]:
        """Get a payment transaction by ID."""
        return self._client.get(f"/v1/transactions/{transaction_id}")

    def list_transactions(self, business_id: str, **filters: Any) -> dict[str, Any]:
        """List payment transactions with optional filters."""
        return self._client.get("/v1/transactions", business_id=business_id, **filters)

    # ── Disbursements ──

    def initiate_disbursement(
        self,
        *,
        business_id: str,
        wallet_id: str,
        amount: str,
        destination_type: str,
        destination_ref: str,
        destination_name: str | None = None,
        currency: str = "RWF",
        description: str | None = None,
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Initiate a disbursement (payout) to a mobile money number."""
        return self._client.post(
            "/v1/disbursements",
            business_id=business_id,
            wallet_id=wallet_id,
            amount=amount,
            destination_type=destination_type,
            destination_ref=destination_ref,
            destination_name=destination_name,
            currency=currency,
            description=description,
            idempotency_key=idempotency_key,
        )

    def get_disbursement(self, disbursement_id: str) -> dict[str, Any]:
        """Get a disbursement by ID."""
        return self._client.get(f"/v1/disbursements/{disbursement_id}")

    def list_disbursements(self, business_id: str, **pagination: Any) -> dict[str, Any]:
        """List disbursements for a business."""
        return self._client.get("/v1/disbursements", business_id=business_id, **pagination)
