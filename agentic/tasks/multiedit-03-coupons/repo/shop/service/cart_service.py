"""Business operations over shopping carts."""
from ..model.cart import Cart
from ..errors import ValidationError


class CartService:
    def __init__(self, cart_store, product_store):
        self.carts = cart_store
        self.products = product_store
        self._seq = 0

    def create_cart(self, owner):
        if not owner:
            raise ValidationError("owner is required")
        self._seq += 1
        cart_id = "cart-%d" % self._seq
        cart = Cart(cart_id, owner)
        self.carts.save(cart)
        return cart

    def add_to_cart(self, cart_id, sku, qty=1):
        cart = self.carts.get(cart_id)
        product = self.products.get(sku)
        cart.add_item(product, qty)
        self.carts.save(cart)
        return cart

    def remove_from_cart(self, cart_id, sku):
        cart = self.carts.get(cart_id)
        cart.remove_item(sku)
        self.carts.save(cart)
        return cart

    def summary(self, cart_id):
        """Return a plain dict describing the cart's current totals."""
        cart = self.carts.get(cart_id)
        return {
            "cart_id": cart.cart_id,
            "owner": cart.owner,
            "item_count": cart.item_count(),
            "subtotal_cents": cart.subtotal_cents(),
            "total_cents": cart.total_cents(),
        }
