# Order Ingestion

This project provides a system for ingesting orders from various sources, including Shopify, Square, and in-store POS.

## Usage

1. Create an instance of the `OrderIngestion` class, passing in instances of the `ShopifyAPI`, `SquareAPI`, and `POSAPI` classes.
2. Call the `ingest_orders` method to pull orders from the APIs and store them in a unified internal schema.

## Testing

Run the tests using `pytest`.
