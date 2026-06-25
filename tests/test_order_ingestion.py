import pytest
from datetime import datetime, timedelta
from order_ingestion import Order, OrderIngestion, ShopifyAPI, SquareAPI, POSAPI, retry_ingestion

def test_pull_orders():
    shopify_api = ShopifyAPI()
    square_api = SquareAPI()
    pos_api = POSAPI()
    ingestion = OrderIngestion(shopify_api, square_api, pos_api)
    orders = ingestion.pull_orders()
    assert len(orders) == 6

def test_store_orders():
    orders = [Order(1, datetime.now(), "Shopify"), Order(2, datetime.now() - timedelta(minutes=10), "Shopify")]
    ingestion = OrderIngestion(None, None, None)
    unified_orders = ingestion.store_orders(orders)
    assert len(unified_orders) == 2
    assert unified_orders[0]["id"] == 1
    assert unified_orders[0]["source"] == "Shopify"

def test_ingest_orders():
    shopify_api = ShopifyAPI()
    square_api = SquareAPI()
    pos_api = POSAPI()
    ingestion = OrderIngestion(shopify_api, square_api, pos_api)
    unified_orders = ingestion.ingest_orders()
    assert len(unified_orders) == 6

def test_retry_ingestion():
    class FailingAPI:
        def pull_orders(self):
            raise Exception("Failed to pull orders")
    ingestion = OrderIngestion(FailingAPI(), FailingAPI(), FailingAPI())
    with pytest.raises(Exception):
        retry_ingestion(ingestion)

def test_retry_ingestion_success():
    shopify_api = ShopifyAPI()
    square_api = SquareAPI()
    pos_api = POSAPI()
    ingestion = OrderIngestion(shopify_api, square_api, pos_api)
    unified_orders = retry_ingestion(ingestion)
    assert len(unified_orders) == 6
