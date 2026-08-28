"""Business operations over the product catalog."""
from ..model.product import Product
from ..model.money import dollars_to_cents


class CatalogService:
    def __init__(self, product_store):
        self.products = product_store

    def add_product(self, sku, name, price_dollars):
        product = Product(sku, name, dollars_to_cents(price_dollars))
        self.products.save(product)
        return product

    def get_product(self, sku):
        return self.products.get(sku)

    def list_products(self):
        return sorted(self.products.all(), key=lambda p: p.sku)
