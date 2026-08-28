"""The Product entity."""
from ..errors import ValidationError


class Product:
    def __init__(self, sku, name, price_cents):
        if not sku:
            raise ValidationError("sku is required")
        if price_cents < 0:
            raise ValidationError("price_cents must be non-negative")
        self.sku = sku
        self.name = name
        self.price_cents = int(price_cents)

    def __repr__(self):
        return "Product(sku=%r, price_cents=%d)" % (self.sku, self.price_cents)
