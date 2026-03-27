"""Core Wistfare HTTP client — transport, auth, and retries."""

from __future__ import annotations

import time
import random
from typing import Any

import httpx

from wistfare.core.errors import (
    WistfareError,
    AuthenticationError,
    PermissionError as WistfarePermissionError,
    NotFoundError,
    ValidationError,
    RateLimitError,
)

_SDK_VERSION = "0.1.0"
_DEFAULT_BASE_URL = "https://api-production.wistfare.com"
_DEFAULT_TIMEOUT = 30.0
_DEFAULT_MAX_RETRIES = 2


class Wistfare:
    """Wistfare API client.

    Usage::

        from wistfare.core import Wistfare
        from wistfare.payments import PaymentsClient
        from wistfare.wallet import WalletClient
        from wistfare.business import BusinessClient

        wf = Wistfare(api_key="wf_live_xxx")
        payments = PaymentsClient(wf)
        wallets = WalletClient(wf)
        business = BusinessClient(wf)

        balance = wallets.get_balance("wal_123")
        collection = payments.initiate_collection(...)
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = _DEFAULT_TIMEOUT,
        max_retries: int = _DEFAULT_MAX_RETRIES,
    ) -> None:
        if not api_key:
            raise WistfareError(
                'API key is required. Pass api_key="wf_live_..." or api_key="wf_test_...".',
                400,
                "missing_api_key",
            )
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self._http = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={
                "X-API-Key": self.api_key,
                "User-Agent": f"wistfare-python/{_SDK_VERSION}",
                "Accept": "application/json",
            },
        )
        self._payments = None
        self._wallet = None
        self._business = None

    @property
    def is_test_mode(self) -> bool:
        return self.api_key.startswith("wf_test_")

    @property
    def payments(self):
        if self._payments is None:
            from wistfare.payments.client import PaymentsClient

            self._payments = PaymentsClient(self)
        return self._payments

    @property
    def wallet(self):
        if self._wallet is None:
            from wistfare.wallet.client import WalletClient

            self._wallet = WalletClient(self)
        return self._wallet

    @property
    def business(self):
        if self._business is None:
            from wistfare.business.client import BusinessClient

            self._business = BusinessClient(self)
        return self._business

    # ── HTTP methods ──

    def request(
        self,
        method: str,
        path: str,
        *,
        json: Any | None = None,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Send an HTTP request with retries and error handling."""
        clean_params = (
            {k: v for k, v in params.items() if v is not None} if params else None
        )
        last_error: Exception | None = None

        for attempt in range(self.max_retries + 1):
            if attempt > 0:
                time.sleep(min(1.0 * 2 ** (attempt - 1), 10.0) + random.random() * 0.5)

            try:
                resp = self._http.request(method, path, json=json, params=clean_params)

                if resp.is_success:
                    if resp.status_code == 204:
                        return None
                    return resp.json()

                request_id = resp.headers.get("x-request-id")
                body = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
                message = body.get("error", {}).get("message", resp.reason_phrase)

                if resp.status_code == 429:
                    retry_after = int(resp.headers.get("retry-after", "5"))
                    if attempt < self.max_retries:
                        time.sleep(retry_after)
                        continue
                    raise RateLimitError(retry_after, request_id)

                if resp.status_code >= 500 and attempt < self.max_retries:
                    last_error = WistfareError(message, resp.status_code, "internal_error", request_id)
                    continue

                raise self._build_error(resp.status_code, message, body, request_id)

            except WistfareError:
                raise
            except Exception as exc:
                last_error = exc
                if attempt >= self.max_retries:
                    break

        raise last_error or WistfareError("Request failed after retries", 500, "internal_error")

    def get(self, path: str, **params: Any) -> Any:
        return self.request("GET", path, params=params if params else None)

    def post(self, path: str, **data: Any) -> Any:
        clean = {k: v for k, v in data.items() if v is not None} if data else None
        return self.request("POST", path, json=clean if clean else None)

    def patch(self, path: str, **data: Any) -> Any:
        clean = {k: v for k, v in data.items() if v is not None} if data else None
        return self.request("PATCH", path, json=clean if clean else None)

    def delete(self, path: str) -> Any:
        return self.request("DELETE", path)

    def close(self) -> None:
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    @staticmethod
    def _build_error(
        status: int, message: str, body: dict, request_id: str | None
    ) -> WistfareError:
        error_details = body.get("error", {})
        match status:
            case 401:
                return AuthenticationError(message, request_id)
            case 403:
                return WistfarePermissionError(message, request_id)
            case 404:
                return NotFoundError(message, request_id)
            case 400 | 422:
                return ValidationError(message, error_details.get("details"), request_id)
            case _:
                return WistfareError(message, status, error_details.get("code", "unknown"), request_id)
