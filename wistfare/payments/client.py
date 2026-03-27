"""Payments API client — collections, disbursements, fees & payment requests."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from wistfare.core.client import Wistfare


# ── Webhooks ──

WebhookEvent = Literal[
    "collection.completed",
    "collection.failed",
    "disbursement.completed",
    "disbursement.failed",
]

WebhookTransactionType = Literal["collection", "disbursement"]


@dataclass(frozen=True)
class WebhookPayload:
    """Payload delivered to your webhook endpoint."""

    event: WebhookEvent
    transaction_id: str
    transaction_type: WebhookTransactionType
    status: str
    amount: str
    fee_amount: str
    net_amount: str
    currency: str
    business_wallet_id: str
    customer_phone: str
    customer_name: str
    payment_method: str
    reference_id: str
    description: str
    failure_reason: str
    timestamp: str


def parse_webhook_payload(body: str | bytes) -> WebhookPayload:
    """Parse a raw webhook request body into a WebhookPayload."""
    raw = body if isinstance(body, str) else body.decode("utf-8")
    data = json.loads(raw)
    return WebhookPayload(
        event=data["event"],
        transaction_id=data["transaction_id"],
        transaction_type=data["transaction_type"],
        status=data["status"],
        amount=data["amount"],
        fee_amount=data["fee_amount"],
        net_amount=data["net_amount"],
        currency=data["currency"],
        business_wallet_id=data["business_wallet_id"],
        customer_phone=data["customer_phone"],
        customer_name=data["customer_name"],
        payment_method=data["payment_method"],
        reference_id=data["reference_id"],
        description=data["description"],
        failure_reason=data.get("failure_reason", ""),
        timestamp=data["timestamp"],
    )


class PaymentsClient:
    """Payments API — collections, disbursements, fee management & payment requests."""

    def __init__(self, client: Wistfare) -> None:
        self._client = client

    # ── Fee Management ──

    def get_fee_config(self, business_id: str, transaction_type: str) -> dict[str, Any]:
        """Get fee configuration for a business and transaction type."""
        return self._client.get(f"/v1/fees/{business_id}", transaction_type=transaction_type)

    def list_fee_configs(
        self,
        business_id: str,
        *,
        page: int | None = None,
        per_page: int | None = None,
    ) -> dict[str, Any]:
        """List all fee configs for a business."""
        params: dict[str, Any] = {"business_id": business_id}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        return self._client.get("/v1/fees", **params)

    # ── Collections ──

    def initiate_collection(
        self,
        *,
        business_id: str,
        wallet_id: str | None = None,
        customer_phone: str,
        amount: str,
        payment_method: str,
        currency: str | None = None,
        description: str | None = None,
        reference_id: str | None = None,
        payment_request_id: str | None = None,
    ) -> dict[str, Any]:
        """Initiate a mobile money collection from a customer."""
        payload: dict[str, Any] = {
            "business_id": business_id,
            "wallet_id": wallet_id,
            "customer_phone": customer_phone,
            "amount": amount,
            "payment_method": payment_method,
            "currency": currency,
            "description": description,
            "reference_id": reference_id,
            "payment_request_id": payment_request_id,
        }
        return self._client.post("/v1/collections", **payload)

    def list_collections(
        self,
        *,
        business_id: str | None = None,
        reference_id: str | None = None,
        status: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> dict[str, Any]:
        """List collections with optional filters."""
        params: dict[str, Any] = {}
        if business_id is not None:
            params["business_id"] = business_id
        if reference_id is not None:
            params["reference_id"] = reference_id
        if status is not None:
            params["status"] = status
        if from_date is not None:
            params["from_date"] = from_date
        if to_date is not None:
            params["to_date"] = to_date
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        return self._client.get("/v1/collections", **params)

    # ── Payment Requests ──

    def create_payment_request(
        self,
        *,
        business_id: str,
        wallet_id: str,
        request_type: str,
        amount: str,
        currency: str | None = None,
        reference_id: str | None = None,
        description: str | None = None,
    ) -> dict[str, Any]:
        """Create a payment request (QR code or payment link)."""
        return self._client.post(
            "/v1/payment-requests",
            business_id=business_id,
            wallet_id=wallet_id,
            request_type=request_type,
            amount=amount,
            currency=currency,
            reference_id=reference_id,
            description=description,
        )

    # ── Disbursements ──

    def initiate_disbursement(
        self,
        *,
        business_id: str,
        wallet_id: str,
        amount: str,
        destination_type: str,
        destination_ref: str,
        currency: str | None = None,
        description: str | None = None,
        reference_id: str | None = None,
    ) -> dict[str, Any]:
        """Initiate a disbursement (payout) to a mobile money number."""
        return self._client.post(
            "/v1/disbursements",
            business_id=business_id,
            wallet_id=wallet_id,
            amount=amount,
            destination_type=destination_type,
            destination_ref=destination_ref,
            currency=currency,
            description=description,
            reference_id=reference_id,
        )
