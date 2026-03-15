"""Tests for wistfare.wallet.client.WalletClient."""

from wistfare.wallet.client import WalletClient


class TestWallets:
    def test_create(self, mock_wistfare):
        wc = WalletClient(mock_wistfare)
        wc.create(user_id="usr_1", wallet_type="personal")
        mock_wistfare.post.assert_called_once_with(
            "/v1/wallets", user_id="usr_1", wallet_type="personal", currency="RWF"
        )

    def test_get(self, mock_wistfare):
        wc = WalletClient(mock_wistfare)
        wc.get("wal_1")
        mock_wistfare.get.assert_called_once_with("/v1/wallets/wal_1")

    def test_get_by_owner(self, mock_wistfare):
        wc = WalletClient(mock_wistfare)
        wc.get_by_owner("usr_1")
        mock_wistfare.get.assert_called_once_with("/v1/wallets/by-owner", user_id="usr_1")

    def test_get_balance(self, mock_wistfare):
        wc = WalletClient(mock_wistfare)
        wc.get_balance("wal_1")
        mock_wistfare.get.assert_called_once_with("/v1/wallets/wal_1/balance")


class TestTransfers:
    def test_transfer(self, mock_wistfare):
        wc = WalletClient(mock_wistfare)
        wc.transfer(
            from_wallet_id="wal_1",
            to_wallet_id="wal_2",
            amount="5000",
            idempotency_key="idk_1",
            description="rent",
        )
        mock_wistfare.post.assert_called_once_with(
            "/v1/wallets/transfers",
            from_wallet_id="wal_1",
            to_wallet_id="wal_2",
            amount="5000",
            idempotency_key="idk_1",
            description="rent",
        )

    def test_list_transactions(self, mock_wistfare):
        wc = WalletClient(mock_wistfare)
        wc.list_transactions("wal_1", page=2)
        mock_wistfare.get.assert_called_once_with("/v1/wallets/wal_1/transactions", page=2)


class TestDepositsWithdrawals:
    def test_initiate_deposit(self, mock_wistfare):
        wc = WalletClient(mock_wistfare)
        wc.initiate_deposit(
            wallet_id="wal_1",
            amount="10000",
            payment_method="mtn",
            phone_number="+250781234567",
        )
        mock_wistfare.post.assert_called_once_with(
            "/v1/wallets/deposits",
            wallet_id="wal_1",
            amount="10000",
            payment_method="mtn",
            phone_number="+250781234567",
            currency="RWF",
        )

    def test_initiate_withdrawal(self, mock_wistfare):
        wc = WalletClient(mock_wistfare)
        wc.initiate_withdrawal(
            wallet_id="wal_1",
            amount="5000",
            destination_type="mobile_money",
            destination_ref="+250781234567",
        )
        mock_wistfare.post.assert_called_once_with(
            "/v1/wallets/withdrawals",
            wallet_id="wal_1",
            amount="5000",
            destination_type="mobile_money",
            destination_ref="+250781234567",
            currency="RWF",
        )


class TestRoles:
    def test_create_role(self, mock_wistfare):
        wc = WalletClient(mock_wistfare)
        wc.create_role(wallet_id="wal_1", name="admin", permissions=["transfer", "withdraw"])
        mock_wistfare.post.assert_called_once_with(
            "/v1/wallets/roles",
            wallet_id="wal_1",
            name="admin",
            permissions=["transfer", "withdraw"],
        )

    def test_list_roles(self, mock_wistfare):
        wc = WalletClient(mock_wistfare)
        wc.list_roles("wal_1")
        mock_wistfare.get.assert_called_once_with("/v1/wallets/wal_1/roles")

    def test_update_role(self, mock_wistfare):
        wc = WalletClient(mock_wistfare)
        wc.update_role("role_1", name="viewer")
        mock_wistfare.patch.assert_called_once_with("/v1/wallets/roles/role_1", name="viewer")

    def test_delete_role(self, mock_wistfare):
        wc = WalletClient(mock_wistfare)
        wc.delete_role("role_1")
        mock_wistfare.delete.assert_called_once_with("/v1/wallets/roles/role_1")


class TestMembers:
    def test_add_member(self, mock_wistfare):
        wc = WalletClient(mock_wistfare)
        wc.add_member(wallet_id="wal_1", user_id="usr_2", role_id="role_1")
        mock_wistfare.post.assert_called_once_with(
            "/v1/wallets/members", wallet_id="wal_1", user_id="usr_2", role_id="role_1"
        )

    def test_list_members(self, mock_wistfare):
        wc = WalletClient(mock_wistfare)
        wc.list_members("wal_1")
        mock_wistfare.get.assert_called_once_with("/v1/wallets/wal_1/members")

    def test_update_member_role(self, mock_wistfare):
        wc = WalletClient(mock_wistfare)
        wc.update_member_role("mem_1", "role_2")
        mock_wistfare.patch.assert_called_once_with("/v1/wallets/members/mem_1", role_id="role_2")

    def test_remove_member(self, mock_wistfare):
        wc = WalletClient(mock_wistfare)
        wc.remove_member("mem_1")
        mock_wistfare.delete.assert_called_once_with("/v1/wallets/members/mem_1")
