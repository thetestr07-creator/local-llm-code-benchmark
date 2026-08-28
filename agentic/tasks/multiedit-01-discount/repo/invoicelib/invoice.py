"""A tiny invoicing model."""
from .money import to_cents, cents_to_str


class LineItem:
    def __init__(self, desc, qty, unit_price):
        self.desc = desc
        self.qty = qty
        self.unit_price = unit_price

    def total_cents(self):
        return self.qty * to_cents(self.unit_price)


class Invoice:
    def __init__(self):
        self.items = []

    def add(self, desc, qty, unit_price):
        self.items.append(LineItem(desc, qty, unit_price))

    def total_cents(self):
        return sum(i.total_cents() for i in self.items)

    def total_str(self):
        return cents_to_str(self.total_cents())
