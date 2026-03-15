"""Tests for wistfare.business.client.BusinessClient."""

from wistfare.business.client import BusinessClient


class TestBusinesses:
    def test_create(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.create(name="My Shop", business_type="retail", country="RW")
        mock_wistfare.post.assert_called_once_with(
            "/v1/businesses", name="My Shop", business_type="retail", country="RW"
        )

    def test_get(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.get("biz_1")
        mock_wistfare.get.assert_called_once_with("/v1/businesses/biz_1")

    def test_list_mine(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.list_mine(page=1)
        mock_wistfare.get.assert_called_once_with("/v1/businesses/mine", page=1)

    def test_update(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.update("biz_1", name="New Name")
        mock_wistfare.patch.assert_called_once_with("/v1/businesses/biz_1", name="New Name")


class TestStaff:
    def test_assign_staff(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.assign_staff(business_id="biz_1", user_id="usr_1", role="cashier")
        mock_wistfare.post.assert_called_once_with(
            "/v1/staff", business_id="biz_1", user_id="usr_1", role="cashier"
        )

    def test_list_staff(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.list_staff("biz_1", page=1)
        mock_wistfare.get.assert_called_once_with("/v1/staff", business_id="biz_1", page=1)

    def test_update_staff_role(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.update_staff_role("staff_1", "manager")
        mock_wistfare.patch.assert_called_once_with("/v1/staff/staff_1/role", role="manager")

    def test_remove_staff(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.remove_staff("staff_1")
        mock_wistfare.delete.assert_called_once_with("/v1/staff/staff_1")


class TestInvitations:
    def test_invite_staff(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.invite_staff(business_id="biz_1", role="cashier", email="a@b.com")
        mock_wistfare.post.assert_called_once_with(
            "/v1/invitations", business_id="biz_1", role="cashier", email="a@b.com", phone=None
        )

    def test_list_invitations(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.list_invitations("biz_1")
        mock_wistfare.get.assert_called_once_with("/v1/invitations", business_id="biz_1")

    def test_accept_invitation(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.accept_invitation("tok_abc")
        mock_wistfare.post.assert_called_once_with("/v1/invitations/accept", token="tok_abc")

    def test_revoke_invitation(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.revoke_invitation("inv_1")
        mock_wistfare.delete.assert_called_once_with("/v1/invitations/inv_1")


class TestTeams:
    def test_create_team(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.create_team(business_id="biz_1", name="Sales")
        mock_wistfare.post.assert_called_once_with("/v1/teams", business_id="biz_1", name="Sales")

    def test_list_teams(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.list_teams("biz_1")
        mock_wistfare.get.assert_called_once_with("/v1/teams", business_id="biz_1")

    def test_update_team(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.update_team("team_1", name="Support")
        mock_wistfare.patch.assert_called_once_with("/v1/teams/team_1", name="Support")

    def test_delete_team(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.delete_team("team_1")
        mock_wistfare.delete.assert_called_once_with("/v1/teams/team_1")

    def test_add_team_member(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.add_team_member("team_1", "usr_1", role="lead")
        mock_wistfare.post.assert_called_once_with("/v1/teams/team_1/members", user_id="usr_1", role="lead")

    def test_remove_team_member(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.remove_team_member("team_1", "usr_1")
        mock_wistfare.delete.assert_called_once_with("/v1/teams/team_1/members/usr_1")


class TestApiKeys:
    def test_create_api_key(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.create_api_key(business_id="biz_1", name="prod-key", environment="live")
        mock_wistfare.post.assert_called_once_with(
            "/v1/api-keys", business_id="biz_1", name="prod-key", environment="live"
        )

    def test_list_api_keys(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.list_api_keys("biz_1")
        mock_wistfare.get.assert_called_once_with("/v1/api-keys", business_id="biz_1")

    def test_revoke_api_key(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.revoke_api_key("key_1")
        mock_wistfare.delete.assert_called_once_with("/v1/api-keys/key_1")
