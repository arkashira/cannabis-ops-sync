import json
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

@dataclass
class Order:
    id: int
    created_at: datetime
    source: str

class OrderIngestion:
    def __init__(self, shopify_api, square_api, pos_api):
        self.shopify_api = shopify_api
        self.square_api = square_api
        self.pos_api = pos_api
        self.logger = logging.getLogger(__name__)

    def pull_orders(self):
        orders = []
        for api in [self.shopify_api, self.square_api, self.pos_api]:
            try:
                orders.extend(api.pull_orders())
            except Exception as e:
                self.logger.error(f"Failed to pull orders from {api.__class__.__name__}: {e}")
                raise
        return orders

    def store_orders(self, orders):
        unified_orders = []
        for order in orders:
            unified_order = {
                "id": order.id,
                "created_at": order.created_at.isoformat(),
                "source": order.source
            }
            unified_orders.append(unified_order)
        return unified_orders

    def ingest_orders(self):
        orders = self.pull_orders()
        unified_orders = self.store_orders(orders)
        return unified_orders

class ShopifyAPI:
    def pull_orders(self):
        # Simulate pulling orders from Shopify API
        return [Order(1, datetime.now(), "Shopify"), Order(2, datetime.now() - timedelta(minutes=10), "Shopify")]

class SquareAPI:
    def pull_orders(self):
        # Simulate pulling orders from Square API
        return [Order(3, datetime.now(), "Square"), Order(4, datetime.now() - timedelta(minutes=5), "Square")]

class POSAPI:
    def pull_orders(self):
        # Simulate pulling orders from POS API
        return [Order(5, datetime.now(), "POS"), Order(6, datetime.now() - timedelta(minutes=15), "POS")]

def retry_ingestion(ingestion, max_retries=3):
    for attempt in range(max_retries + 1):
        try:
            return ingestion.ingest_orders()
        except Exception as e:
            if attempt < max_retries:
                logging.error(f"Ingestion failed (attempt {attempt + 1}/{max_retries + 1}): {e}")
            else:
                logging.error(f"Ingestion failed after {max_retries} retries: {e}")
                raise
