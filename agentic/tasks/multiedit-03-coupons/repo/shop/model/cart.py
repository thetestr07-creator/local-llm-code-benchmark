"""The Cart entity and its line items."""
from ..errors import ValidationError, NotFound


class CartLine:
    def __init__(self, product, qty):
        self.product = product
        self.qty = int(qty)

    def subtotal_cents(self):
        return self.product.price_cents * self.qty


class Cart:
    def __init__(self, cart_id, owner):
        self.cart_id = cart_id
        self.owner = owner
        self.lines = []

    def add_item(self, product, qty=1):
        if qty <= 0:
            raise ValidationError("qty must be positive")
        for line in self.lines:
            if line.product.sku == product.sku:
                line.qty += qty
                return line
        line = CartLine(product, qty)
        self.lines.append(line)
        return line

    def remove_item(self, sku):
        for i, line in enumerate(self.lines):
            if line.product.sku == sku:
                del self.lines[i]
                return
        raise NotFound("no line for sku %r" % sku)

    def item_count(self):
        return sum(line.qty for line in self.lines)

    def subtotal_cents(self):
        """Sum of all line subtotals, before any discounts."""
        return sum(line.subtotal_cents() for line in self.lines)

    def total_cents(self):
        """The amount owed. Without any discount this equals the subtotal."""
        return self.subtotal_cents()
