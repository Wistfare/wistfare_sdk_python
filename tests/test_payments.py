"""Tests for wistfare.payments.client.PaymentsClient."""

from wistfare.payments.client import PaymentsClient


class TestFeeManagement:
    def test_set_fee_config(self, mock_wistfare):
        pc = PaymentsClient(mock_wistfare)
        pc.set_fee_config(
            business_id="biz_1",
            transaction_type="collection",
            fee_model="percentage",
            percentage_rate="2.5",
            currency="RWF",
        )
        mock_wistfare.post.assert_called_once_with(
            "/v1/fees",
            business_id="biz_1",
            transaction_type="collection",
            fee_model="percentage",
            percentage_rate="2.5",
            flat_amount=None,
            min_fee=None,
            max_fee=None,
            currency="RWF",
        )

    def test_get_fee_config(self, mock_wistfare):
        pc = PaymentsClient(mock_wistfare)
        pc.get_fee_config("biz_1", "collection")
        mock_wistfare.get.assert_called_once_with("/v1/fees/biz_1", transaction_type="collection")

    def test_list_fee_configs(self, mock_wistfare):
        pc = PaymentsClient(mock_wistfare)
        pc.list_fee_configs("biz_1", page=2)
        mock_wistfare.get.assert_called_once_with("/v1/fees", business_id="biz_1", page=2)

    def test_delete_fee_config(self, mock_wistfare):
        pc = PaymentsClient(mock_wistfare)
        pc.delete_fee_config("fee_1")
        mock_wistfare.delete.assert_called_once_with("/v1/fees/fee_1")

    def test_calculate_fee(self, mock_wistfare):
        pc = PaymentsClient(mock_wistfare)
        pc.calculate_fee(business_id="biz_1", amount="10000", transaction_type="collection")
        mock_wistfare.post.assert_called_once_with(
            "/v1/fees/calculate",
            business_id="biz_1",
            amount="10000",
            transaction_type="collection",
            currency="RWF",
        )


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
            currency="RWF",
            description=None,
            customer_phone=None,
            customer_name=None,
            max_uses=None,
            expires_at=None,
        )

    def test_get_payment_request(self, mock_wistfare):
        pc = PaymentsClient(mock_wistfare)
        pc.get_payment_request("pr_1")
        mock_wistfare.get.assert_called_once_with("/v1/payment-requests/pr_1")

    def test_list_payment_requests(self, mock_wistfare):
        pc = PaymentsClient(mock_wistfare)
        pc.list_payment_requests("biz_1", limit=10)
        mock_wistfare.get.assert_called_once_with("/v1/payment-requests", business_id="biz_1", limit=10)

    def test_cancel_payment_request(self, mock_wistfare):
        pc = PaymentsClient(mock_wistfare)
        pc.cancel_payment_request("pr_1")
        mock_wistfare.post.assert_called_once_with("/v1/payment-requests/pr_1/cancel")


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
            currency="RWF",
            description=None,
            external_id=None,
        )


class TestTransactions:
    def test_get_transaction(self, mock_wistfare):
        pc = PaymentsClient(mock_wistfare)
        pc.get_transaction("txn_1")
        mock_wistfare.get.assert_called_once_with("/v1/transactions/txn_1")

    def test_list_transactions(self, mock_wistfare):
        pc = PaymentsClient(mock_wistfare)
        pc.list_transactions("biz_1", status="completed")
        mock_wistfare.get.assert_called_once_with("/v1/transactions", business_id="biz_1", status="completed")


class TestDisbursements:
    def test_initiate_disbursement(self, mock_wistfare):
        pc = PaymentsClient(mock_wistfare)
        pc.initiate_disbursement(
            business_id="biz_1",
            wallet_id="wal_1",
            amount="5000",
            destination_type="mobile_money",
            destination_ref="+250781234567",
            idempotency_key="idk_1",
        )
        mock_wistfare.post.assert_called_once_with(
            "/v1/disbursements",
            business_id="biz_1",
            wallet_id="wal_1",
            amount="5000",
            destination_type="mobile_money",
            destination_ref="+250781234567",
            destination_name=None,
            currency="RWF",
            description=None,
            idempotency_key="idk_1",
        )

    def test_get_disbursement(self, mock_wistfare):
        pc = PaymentsClient(mock_wistfare)
        pc.get_disbursement("disb_1")
        mock_wistfare.get.assert_called_once_with("/v1/disbursements/disb_1")

    def test_list_disbursements(self, mock_wistfare):
        pc = PaymentsClient(mock_wistfare)
        pc.list_disbursements("biz_1", page=1)
        mock_wistfare.get.assert_called_once_with("/v1/disbursements", business_id="biz_1", page=1)
