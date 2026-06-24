from src.axentx_product.product import Product
from src.axentx_product.validation import validate_product

def test_product_creation():
    product = Product("Test Product", 10)
    assert str(product) == "Product 'Test Product' with demand 10"

def test_product_validation():
    product = Product("Test Product", 10)
    assert validate_product(product) is True

def test_product_validation_zero_demand():
    product = Product("Test Product", 0)
    assert validate_product(product) is False

def test_product_validation_negative_demand():
    product = Product("Test Product", -10)
    assert validate_product(product) is False
