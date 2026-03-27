"""Tests for wistfare.payments.client.PaymentsClient."""

from wistfare.payments.client import PaymentsClient


class TestFeeManagement:
    def test_get_fee_config(self, mock_wistfare):
        pc = PaymentsClient(mock_wistfare)
        pc.get_fee_config("biz_1", "collection")
        mock_wistfare.get.assert_called_once_with("/v1/fees/biz_1", transaction_type="collection")

    def test_list_fee_configs(self, mock_wistfare):
        pc = PaymentsClient(mock_wistfare)
        pc.list_fee_configs("biz_1", page=2)
        mock_wistfare.get.assert_called_once_with("/v1/fees", business_id="biz_1", page=2)

    def test_list_fee_configs_no_pagination(self, mock_wistfare):
        pc = PaymentsClient(mock_wistfare)
        pc.list_fee_configs("biz_1")
        mock_wistfare.get.assert_called_once_with("/v1/fees", business_id="biz_1")


class TestCollections:
    def test_initiate_collection(self, mock_wistfare):
        pc = PaymentsClient(mock_wistfare)
        pc.initiate_collection(
            business_id="biz_1",
            wallet_id="wal_1",
            customer_phone="+250781234567",
            amount="10000",
            payment_method="mtn",
        )
        mock_wistfare.post.assert_called_once_with(
            "/v1/collections",
            business_id="biz_1",
            wallet_id="wal_1",
            customer_phone="+250781234567",
            amount="10000",
            payment_method="mtn",
            currency=None,
            description=None,
            reference_id=None,
            payment_request_id=None,
        )

    def test_list_collections(self, mock_wistfare):
        pc = PaymentsClient(mock_wistfare)
        pc.list_collections(business_id="biz_1", status="completed")
        mock_wistfare.get.assert_called_once_with(
            "/v1/collections", business_id="biz_1", status="completed"
        )

    def test_list_collections_no_filters(self, mock_wistfare):
        pc = PaymentsClient(mock_wistfare)
        pc.list_collections()
        mock_wistfare.get.assert_called_once_with("/v1/collections")


class TestPaymentRequests:
    def test_create_payment_request(self, mock_wistfare):
        pc = PaymentsClient(mock_wistfare)
        pc.create_payment_request(
            business_id="biz_1",
            wallet_id="wal_1",
            request_type="qr",
            amount="5000",
        )
        mock_wistfare.post.assert_called_once_with(
            "/v1/payment-requests",
            business_id="biz_1",
            wallet_id="wal_1",
            request_type="qr",
            amount="5000",
            currency=None,
            reference_id=None,
            description=None,
        )


class TestDisbursements:
    def test_initiate_disbursement(self, mock_wistfare):
        pc = PaymentsClient(mock_wistfare)
        pc.initiate_disbursement(
            business_id="biz_1",
            wallet_id="wal_1",
            amount="5000",
            destination_type="mobile_money",
            destination_ref="+250781234567",
        )
        mock_wistfare.post.assert_called_once_with(
            "/v1/disbursements",
            business_id="biz_1",
            wallet_id="wal_1",
            amount="5000",
            destination_type="mobile_money",
            destination_ref="+250781234567",
            currency=None,
            description=None,
            reference_id=None,
        )
