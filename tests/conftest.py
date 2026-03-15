"""Shared fixtures for Wistfare SDK tests."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from wistfare.client import Wistfare


@pytest.fixture()
def mock_http():
    """Patch httpx.Client so no real HTTP connections are made."""
    with patch("wistfare.client.httpx.Client") as mock_cls:
        yield mock_cls.return_value


@pytest.fixture()
def client(mock_http):
    """Return a Wistfare client wired to the mocked httpx.Client."""
    return Wistfare(api_key="wf_test_key123")


@pytest.fixture()
def live_client(mock_http):
    """Return a Wistfare client with a live-mode API key."""
    return Wistfare(api_key="wf_live_key456")


@pytest.fixture()
def mock_wistfare():
    """Return a MagicMock that quacks like a Wistfare client (for service-client tests)."""
    m = MagicMock(spec=Wistfare)
    m.get = MagicMock(return_value={"ok": True})
    m.post = MagicMock(return_value={"ok": True})
    m.patch = MagicMock(return_value={"ok": True})
    m.delete = MagicMock(return_value=None)
    return m
