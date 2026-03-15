"""Tests for wistfare.errors."""

from wistfare.errors import (
    WistfareError,
    AuthenticationError,
    PermissionError as WistfarePermissionError,
    NotFoundError,
    ValidationError,
    RateLimitError,
)


class TestWistfareError:
    def test_attributes(self):
        err = WistfareError("boom", 500, "internal_error", "req_1")
        assert str(err) == "boom"
        assert err.status == 500
        assert err.code == "internal_error"
        assert err.request_id == "req_1"

    def test_request_id_defaults_none(self):
        err = WistfareError("x", 400, "bad")
        assert err.request_id is None

    def test_is_exception(self):
        assert issubclass(WistfareError, Exception)


class TestAuthenticationError:
    def test_defaults(self):
        err = AuthenticationError()
        assert err.status == 401
        assert err.code == "authentication_error"
        assert "API key" in str(err)

    def test_custom_message(self):
        err = AuthenticationError("nope", "req_2")
        assert str(err) == "nope"
        assert err.request_id == "req_2"

    def test_isinstance(self):
        assert isinstance(AuthenticationError(), WistfareError)


class TestPermissionError:
    def test_defaults(self):
        err = WistfarePermissionError()
        assert err.status == 403
        assert err.code == "permission_error"

    def test_isinstance(self):
        assert isinstance(WistfarePermissionError(), WistfareError)


class TestNotFoundError:
    def test_defaults(self):
        err = NotFoundError()
        assert err.status == 404
        assert err.code == "not_found"

    def test_isinstance(self):
        assert isinstance(NotFoundError(), WistfareError)


class TestValidationError:
    def test_defaults(self):
        err = ValidationError("bad input")
        assert err.status == 400
        assert err.code == "validation_error"
        assert err.errors == {}

    def test_with_errors_dict(self):
        details = {"amount": ["must be positive"]}
        err = ValidationError("invalid", details, "req_3")
        assert err.errors == details
        assert err.request_id == "req_3"

    def test_isinstance(self):
        assert isinstance(ValidationError("x"), WistfareError)


class TestRateLimitError:
    def test_attributes(self):
        err = RateLimitError(30, "req_4")
        assert err.status == 429
        assert err.code == "rate_limit"
        assert err.retry_after == 30
        assert "30s" in str(err)

    def test_isinstance(self):
        assert isinstance(RateLimitError(5), WistfareError)
