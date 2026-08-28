"""Persistence for Cart entities, keyed by cart_id."""
from .base import InMemoryCollection


class CartStore:
    def __init__(self):
        self._c = InMemoryCollection()

    def save(self, cart):
        return self._c.put(cart.cart_id, cart)

    def get(self, cart_id):
        return self._c.get(cart_id)

    def exists(self, cart_id):
        return self._c.has(cart_id)

    def all(self):
        return self._c.all()
