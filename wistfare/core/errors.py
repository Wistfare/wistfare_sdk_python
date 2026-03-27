"""Wistfare SDK error types."""

from __future__ import annotations


class WistfareError(Exception):
    """Base error for all Wistfare API errors."""

    def __init__(
        self,
        message: str,
        status: int,
        code: str,
        request_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.request_id = request_id


class AuthenticationError(WistfareError):
    def __init__(self, message: str = "Invalid or expired API key", request_id: str | None = None):
        super().__init__(message, 401, "authentication_error", request_id)


class PermissionError(WistfareError):  # noqa: A001
    def __init__(self, message: str = "Insufficient permissions", request_id: str | None = None):
        super().__init__(message, 403, "permission_error", request_id)


class NotFoundError(WistfareError):
    def __init__(self, message: str = "Resource not found", request_id: str | None = None):
        super().__init__(message, 404, "not_found", request_id)


class ValidationError(WistfareError):
    def __init__(
        self,
        message: str,
        errors: dict[str, list[str]] | None = None,
        request_id: str | None = None,
    ):
        super().__init__(message, 400, "validation_error", request_id)
        self.errors = errors or {}


class RateLimitError(WistfareError):
    def __init__(self, retry_after: int, request_id: str | None = None):
        super().__init__(f"Rate limit exceeded. Retry after {retry_after}s", 429, "rate_limit", request_id)
        self.retry_after = retry_after
