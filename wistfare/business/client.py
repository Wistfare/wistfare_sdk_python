"""Business API client — business management, staff, teams & API keys."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from wistfare.client import Wistfare


class BusinessClient:
    """Business API — manage businesses, staff, teams & API keys."""

    def __init__(self, client: Wistfare) -> None:
        self._client = client

    # ── Businesses ──

    def create(self, *, name: str, business_type: str, **kwargs: Any) -> dict[str, Any]:
        """Create a new business."""
        return self._client.post("/v1/businesses", name=name, business_type=business_type, **kwargs)

    def get(self, business_id: str) -> dict[str, Any]:
        """Get a business by ID."""
        return self._client.get(f"/v1/businesses/{business_id}")

    def list_mine(self, **pagination: Any) -> dict[str, Any]:
        """List businesses owned by the current user."""
        return self._client.get("/v1/businesses/mine", **pagination)

    def update(self, business_id: str, **params: Any) -> dict[str, Any]:
        """Update a business."""
        return self._client.patch(f"/v1/businesses/{business_id}", **params)

    # ── Staff ──

    def assign_staff(self, *, business_id: str, user_id: str, role: str, **kwargs: Any) -> dict[str, Any]:
        """Assign a user as staff to a business."""
        return self._client.post("/v1/staff", business_id=business_id, user_id=user_id, role=role, **kwargs)

    def list_staff(self, business_id: str, **pagination: Any) -> dict[str, Any]:
        """List staff members of a business."""
        return self._client.get("/v1/staff", business_id=business_id, **pagination)

    def update_staff_role(self, staff_id: str, role: str) -> None:
        """Update a staff member's role."""
        self._client.patch(f"/v1/staff/{staff_id}/role", role=role)

    def remove_staff(self, staff_id: str) -> None:
        """Remove a staff member."""
        self._client.delete(f"/v1/staff/{staff_id}")

    # ── Invitations ──

    def invite_staff(self, *, business_id: str, role: str, email: str | None = None, phone: str | None = None) -> dict[str, Any]:
        """Invite a user to join a business as staff."""
        return self._client.post("/v1/invitations", business_id=business_id, role=role, email=email, phone=phone)

    def list_invitations(self, business_id: str, **pagination: Any) -> dict[str, Any]:
        """List pending invitations for a business."""
        return self._client.get("/v1/invitations", business_id=business_id, **pagination)

    def accept_invitation(self, token: str) -> dict[str, Any]:
        """Accept a staff invitation."""
        return self._client.post("/v1/invitations/accept", token=token)

    def revoke_invitation(self, invitation_id: str) -> None:
        """Revoke a pending invitation."""
        self._client.delete(f"/v1/invitations/{invitation_id}")

    # ── Teams ──

    def create_team(self, *, business_id: str, name: str, **kwargs: Any) -> dict[str, Any]:
        """Create a team within a business."""
        return self._client.post("/v1/teams", business_id=business_id, name=name, **kwargs)

    def list_teams(self, business_id: str, **pagination: Any) -> dict[str, Any]:
        """List teams in a business."""
        return self._client.get("/v1/teams", business_id=business_id, **pagination)

    def update_team(self, team_id: str, **params: Any) -> dict[str, Any]:
        """Update a team."""
        return self._client.patch(f"/v1/teams/{team_id}", **params)

    def delete_team(self, team_id: str) -> None:
        """Delete a team."""
        self._client.delete(f"/v1/teams/{team_id}")

    def add_team_member(self, team_id: str, user_id: str, role: str | None = None) -> dict[str, Any]:
        """Add a member to a team."""
        return self._client.post(f"/v1/teams/{team_id}/members", user_id=user_id, role=role)

    def remove_team_member(self, team_id: str, user_id: str) -> None:
        """Remove a member from a team."""
        self._client.delete(f"/v1/teams/{team_id}/members/{user_id}")

    # ── API Keys ──

    def create_api_key(self, *, business_id: str, name: str, environment: str = "test") -> dict[str, Any]:
        """Create an API key for a business. The raw key is only returned once."""
        return self._client.post("/v1/api-keys", business_id=business_id, name=name, environment=environment)

    def list_api_keys(self, business_id: str) -> dict[str, Any]:
        """List API keys for a business (keys are masked)."""
        return self._client.get("/v1/api-keys", business_id=business_id)

    def revoke_api_key(self, api_key_id: str) -> None:
        """Revoke an API key."""
        self._client.delete(f"/v1/api-keys/{api_key_id}")
