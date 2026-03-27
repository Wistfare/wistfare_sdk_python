"""Tests for wistfare.business.client.BusinessClient."""

from wistfare.business.client import BusinessClient


class TestBusinesses:
    def test_get(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.get("biz_1")
        mock_wistfare.get.assert_called_once_with("/v1/businesses/biz_1")

    def test_list(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.list(business_id="biz_123", page=1)
        mock_wistfare.get.assert_called_once_with("/v1/businesses", business_id="biz_123", page=1)

    def test_list_no_filters(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.list()
        mock_wistfare.get.assert_called_once_with("/v1/businesses")

    def test_list_with_per_page(self, mock_wistfare):
        bc = BusinessClient(mock_wistfare)
        bc.list(page=2, per_page=25)
        mock_wistfare.get.assert_called_once_with("/v1/businesses", page=2, per_page=25)
