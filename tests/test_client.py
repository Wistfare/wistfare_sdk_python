"""Tests for wistfare.client.Wistfare."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import httpx
import pytest

from wistfare.client import Wistfare
from wistfare.errors import (
    WistfareError,
    AuthenticationError,
    PermissionError as WistfarePermissionError,
    NotFoundError,
    ValidationError,
    RateLimitError,
)
from wistfare.payments.client import PaymentsClient
from wistfare.wallet.client import WalletClient
from wistfare.business.client import BusinessClient


# ── Constructor ──


class TestConstructor:
    def test_empty_api_key_raises(self):
        with pytest.raises(WistfareError, match="API key is required"):
            Wistfare(api_key="")

    def test_none_api_key_raises(self, mock_http):
        # Falsy string
        with pytest.raises(WistfareError):
            Wistfare(api_key="")

    def test_stores_api_key(self, client):
        assert client.api_key == "wf_test_key123"

    def test_trailing_slash_stripped(self, mock_http):
        c = Wistfare(api_key="wf_test_x", base_url="https://example.com/")
        assert c.base_url == "https://example.com"

    def test_default_base_url(self, client):
        assert client.base_url == "https://api.wistfare.com"

    def test_default_timeout(self, client):
        assert client.timeout == 30.0

    def test_default_max_retries(self, client):
        assert client.max_retries == 2

    def test_custom_config(self, mock_http):
        c = Wistfare(api_key="wf_test_x", timeout=10.0, max_retries=5)
        assert c.timeout == 10.0
        assert c.max_retries == 5


# ── Properties ──


class TestIsTestMode:
    def test_test_key(self, client):
        assert client.is_test_mode is True

    def test_live_key(self, live_client):
        assert live_client.is_test_mode is False


# ── Service Accessors ──


class TestServiceAccessors:
    def test_payments_type(self, client):
        assert isinstance(client.payments, PaymentsClient)

    def test_wallet_type(self, client):
        assert isinstance(client.wallet, WalletClient)

    def test_business_type(self, client):
        assert isinstance(client.business, BusinessClient)

    def test_payments_cached(self, client):
        p1 = client.payments
        p2 = client.payments
        assert p1 is p2

    def test_wallet_cached(self, client):
        assert client.wallet is client.wallet

    def test_business_cached(self, client):
        assert client.business is client.business


# ── Context Manager ──


class TestContextManager:
    def test_enter_returns_self(self, client):
        assert client.__enter__() is client

    def test_exit_closes(self, client, mock_http):
        client.__exit__(None, None, None)
        mock_http.close.assert_called_once()


# ── Request Method ──


def _make_response(status_code, json_body=None, headers=None, reason="OK"):
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    resp.is_success = 200 <= status_code < 300
    resp.reason_phrase = reason
    resp.headers = headers or {"content-type": "application/json"}
    if json_body is not None:
        resp.json.return_value = json_body
    return resp


class TestRequest:
    def test_sends_correct_method_and_path(self, client, mock_http):
        mock_http.request.return_value = _make_response(200, {"data": 1})
        client.request("GET", "/v1/test")
        mock_http.request.assert_called_once_with("GET", "/v1/test", json=None, params=None)

    def test_passes_json_body(self, client, mock_http):
        mock_http.request.return_value = _make_response(200, {"id": "x"})
        client.request("POST", "/v1/items", json={"name": "thing"})
        mock_http.request.assert_called_once_with("POST", "/v1/items", json={"name": "thing"}, params=None)

    def test_filters_none_params(self, client, mock_http):
        mock_http.request.return_value = _make_response(200, {"ok": True})
        client.request("GET", "/v1/x", params={"a": 1, "b": None})
        mock_http.request.assert_called_once_with("GET", "/v1/x", json=None, params={"a": 1})

    def test_successful_json_response(self, client, mock_http):
        mock_http.request.return_value = _make_response(200, {"balance": "1000"})
        result = client.request("GET", "/v1/balance")
        assert result == {"balance": "1000"}

    def test_204_returns_none(self, client, mock_http):
        mock_http.request.return_value = _make_response(204)
        result = client.request("DELETE", "/v1/item/1")
        assert result is None

    def test_get_convenience(self, client, mock_http):
        mock_http.request.return_value = _make_response(200, {"ok": True})
        client.get("/v1/test", foo="bar")
        mock_http.request.assert_called_once_with("GET", "/v1/test", json=None, params={"foo": "bar"})

    def test_post_convenience(self, client, mock_http):
        mock_http.request.return_value = _make_response(200, {"ok": True})
        client.post("/v1/test", name="x")
        mock_http.request.assert_called_once_with("POST", "/v1/test", json={"name": "x"}, params=None)

    def test_delete_convenience(self, client, mock_http):
        mock_http.request.return_value = _make_response(204)
        client.delete("/v1/test/1")
        mock_http.request.assert_called_once_with("DELETE", "/v1/test/1", json=None, params=None)


# ── Error Mapping ──


class TestErrorMapping:
    def _setup_error(self, mock_http, status, body=None, headers=None):
        body = body or {"error": {"message": "fail"}}
        headers = headers or {"content-type": "application/json"}
        mock_http.request.return_value = _make_response(status, body, headers, reason="Error")

    def test_401_raises_authentication_error(self, client, mock_http):
        self._setup_error(mock_http, 401)
        with pytest.raises(AuthenticationError):
            client.request("GET", "/v1/x")

    def test_403_raises_permission_error(self, client, mock_http):
        self._setup_error(mock_http, 403)
        with pytest.raises(WistfarePermissionError):
            client.request("GET", "/v1/x")

    def test_404_raises_not_found_error(self, client, mock_http):
        self._setup_error(mock_http, 404)
        with pytest.raises(NotFoundError):
            client.request("GET", "/v1/x")

    def test_400_raises_validation_error(self, client, mock_http):
        self._setup_error(mock_http, 400, {"error": {"message": "bad", "details": {"field": ["required"]}}})
        with pytest.raises(ValidationError) as exc_info:
            client.request("POST", "/v1/x")
        assert exc_info.value.errors == {"field": ["required"]}

    def test_422_raises_validation_error(self, client, mock_http):
        self._setup_error(mock_http, 422, {"error": {"message": "unprocessable"}})
        with pytest.raises(ValidationError):
            client.request("POST", "/v1/x")

    def test_429_raises_rate_limit_error(self, client, mock_http):
        # max_retries=2 means 3 attempts; all return 429.
        resp = _make_response(429, {"error": {"message": "slow down"}},
                              {"content-type": "application/json", "retry-after": "1", "x-request-id": "r1"})
        mock_http.request.return_value = resp
        # Override max_retries to 0 to avoid sleep in tests
        client.max_retries = 0
        with pytest.raises(RateLimitError) as exc_info:
            client.request("GET", "/v1/x")
        assert exc_info.value.retry_after == 1


# ── Retry Logic ──


class TestRetryLogic:
    @patch("wistfare.client.time.sleep")
    @patch("wistfare.client.random.random", return_value=0.1)
    def test_retries_on_500(self, mock_rand, mock_sleep, client, mock_http):
        err_resp = _make_response(500, {"error": {"message": "oops"}},
                                  {"content-type": "application/json"}, reason="Server Error")
        ok_resp = _make_response(200, {"ok": True})
        mock_http.request.side_effect = [err_resp, ok_resp]
        result = client.request("GET", "/v1/flaky")
        assert result == {"ok": True}
        assert mock_http.request.call_count == 2

    @patch("wistfare.client.time.sleep")
    @patch("wistfare.client.random.random", return_value=0.1)
    def test_exhausted_retries_raises(self, mock_rand, mock_sleep, client, mock_http):
        err_resp = _make_response(500, {"error": {"message": "down"}},
                                  {"content-type": "application/json"}, reason="Server Error")
        mock_http.request.return_value = err_resp
        with pytest.raises(WistfareError, match="down"):
            client.request("GET", "/v1/down")
        # 1 initial + 2 retries = 3
        assert mock_http.request.call_count == 3

    @patch("wistfare.client.time.sleep")
    @patch("wistfare.client.random.random", return_value=0.1)
    def test_retries_on_connection_error(self, mock_rand, mock_sleep, client, mock_http):
        ok_resp = _make_response(200, {"ok": True})
        mock_http.request.side_effect = [ConnectionError("net"), ok_resp]
        result = client.request("GET", "/v1/retry")
        assert result == {"ok": True}
