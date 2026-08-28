"""Persistence for Product entities, keyed by sku."""
from .base import InMemoryCollection


class ProductStore:
    def __init__(self):
        self._c = InMemoryCollection()

    def save(self, product):
        return self._c.put(product.sku, product)

    def get(self, sku):
        return self._c.get(sku)

    def exists(self, sku):
        return self._c.has(sku)

    def all(self):
        return self._c.all()
