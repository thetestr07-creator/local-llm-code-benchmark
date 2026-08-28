import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shop.factory import build_app
from shop.api.dto import ApiRequest

app = build_app()

# seed a product
r = app.handle(ApiRequest("add_product", {"sku": "A1", "name": "Widget", "price_dollars": 5.00}))
assert r.status == 200, r

# create a cart, add items
r = app.handle(ApiRequest("create_cart", {"owner": "alice"}))
assert r.status == 200, r
cart_id = r.body["cart_id"]

r = app.handle(ApiRequest("add_to_cart", {"cart_id": cart_id, "sku": "A1", "qty": 3}))
assert r.status == 200, r
assert r.body["subtotal_cents"] == 1500, r.body
assert r.body["total_cents"] == 1500, r.body

# unknown product -> 404
r = app.handle(ApiRequest("add_to_cart", {"cart_id": cart_id, "sku": "NOPE"}))
assert r.status == 404, r

# unknown action -> 404
r = app.handle(ApiRequest("frobnicate", {}))
assert r.status == 404, r

print("smoke OK")
