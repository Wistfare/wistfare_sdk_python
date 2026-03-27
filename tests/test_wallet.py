"""Tests for wistfare.wallet.client.WalletClient."""

from wistfare.wallet.client import WalletClient


class TestWallets:
    def test_get_by_wallet_id(self, mock_wistfare):
        wc = WalletClient(mock_wistfare)
        wc.get(wallet_id="wal_1")
        mock_wistfare.get.assert_called_once_with("/v1/wallets", wallet_id="wal_1")

    def test_get_by_owner_id(self, mock_wistfare):
        wc = WalletClient(mock_wistfare)
        wc.get(owner_id="usr_1")
        mock_wistfare.get.assert_called_once_with("/v1/wallets", owner_id="usr_1")

    def test_get_no_params(self, mock_wistfare):
        wc = WalletClient(mock_wistfare)
        wc.get()
        mock_wistfare.get.assert_called_once_with("/v1/wallets")


class TestTransfers:
    def test_transfer(self, mock_wistfare):
        wc = WalletClient(mock_wistfare)
        wc.transfer(
            from_wallet_id="wal_1",
            to_wallet_id="wal_2",
            amount="5000",
            reference_id="ref_1",
            description="rent",
        )
        mock_wistfare.post.assert_called_once_with(
            "/v1/wallets/transfers",
            from_wallet_id="wal_1",
            to_wallet_id="wal_2",
            amount="5000",
            reference_id="ref_1",
            description="rent",
        )

    def test_transfer_no_description(self, mock_wistfare):
        wc = WalletClient(mock_wistfare)
        wc.transfer(
            from_wallet_id="wal_1",
            to_wallet_id="wal_2",
            amount="5000",
            reference_id="ref_1",
        )
        mock_wistfare.post.assert_called_once_with(
            "/v1/wallets/transfers",
            from_wallet_id="wal_1",
            to_wallet_id="wal_2",
            amount="5000",
            reference_id="ref_1",
            description=None,
        )
