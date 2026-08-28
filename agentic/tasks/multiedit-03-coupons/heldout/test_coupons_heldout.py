"""HELD-OUT verification for multiedit-03. The model under test never sees this."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shop.errors import ValidationError, NotFound
from shop.model.coupon import Coupon
from shop.model.product import Product
from shop.model.cart import Cart
from shop.store.coupon_store import CouponStore
from shop.factory import build_app
from shop.api.dto import ApiRequest

# ---------------------------------------------------------------- model: Coupon
c = Coupon("SAVE10", "percent", 10)
assert c.discount_for(1500) == 150, c.discount_for(1500)      # round(150.0)
assert c.discount_for(999) == 100, c.discount_for(999)        # round(99.9)
assert Coupon("Z", "percent", 0).discount_for(1500) == 0
assert Coupon("Z", "percent", 100).discount_for(1500) == 1500

f = Coupon("TAKE20", "fixed", 2000)                            # 2000 cents off
assert f.discount_for(1500) == 1500, f.discount_for(1500)     # capped at subtotal
assert f.discount_for(5000) == 2000, f.discount_for(5000)
assert Coupon("Z", "fixed", 0).discount_for(1500) == 0

# discount never negative / never exceeds subtotal
assert Coupon("Z", "percent", 100).discount_for(0) == 0
assert Coupon("Z", "fixed", 100).discount_for(0) == 0

# ---------------------------------------------------------------- model: validation
for bad in ("", None):
    try:
        Coupon(bad, "percent", 10); raise AssertionError("empty code accepted")
    except ValidationError:
        pass
try:
    Coupon("X", "bogus", 10); raise AssertionError("bad kind accepted")
except ValidationError:
    pass
for badpct in (-1, 101, 200):
    try:
        Coupon("X", "percent", badpct); raise AssertionError("bad percent accepted %r" % badpct)
    except ValidationError:
        pass
try:
    Coupon("X", "fixed", -5); raise AssertionError("negative fixed accepted")
except ValidationError:
    pass

# ---------------------------------------------------------------- model: Cart wiring
cart = Cart("cart-x", "alice")
cart.add_item(Product("A1", "Widget", 500), 3)                 # subtotal 1500
assert cart.subtotal_cents() == 1500
assert cart.coupon is None
assert cart.discount_cents() == 0
assert cart.total_cents() == 1500                              # unchanged w/o coupon
cart.apply_coupon(Coupon("SAVE10", "percent", 10))
assert cart.discount_cents() == 150
assert cart.total_cents() == 1350
cart.apply_coupon(None)                                        # clear
assert cart.discount_cents() == 0
assert cart.total_cents() == 1500

# ---------------------------------------------------------------- store
store = CouponStore()
store.save(Coupon("SAVE10", "percent", 10))
assert store.exists("SAVE10") is True
assert store.exists("NOPE") is False
assert store.get("SAVE10").code == "SAVE10"
try:
    store.get("NOPE"); raise AssertionError("missing coupon did not raise")
except NotFound:
    pass

# ---------------------------------------------------------------- full stack via API
app = build_app()
assert app.handle(ApiRequest("add_product",
    {"sku": "A1", "name": "Widget", "price_dollars": 5.00})).status == 200
cid = app.handle(ApiRequest("create_cart", {"owner": "alice"})).body["cart_id"]
r = app.handle(ApiRequest("add_to_cart", {"cart_id": cid, "sku": "A1", "qty": 3}))
assert r.status == 200 and r.body["subtotal_cents"] == 1500, r.body
assert r.body["total_cents"] == 1500 and r.body["discount_cents"] == 0, r.body

# register + apply a percent coupon through the API
r = app.handle(ApiRequest("register_coupon", {"code": "SAVE10", "kind": "percent", "value": 10}))
assert r.status == 200, r
r = app.handle(ApiRequest("apply_coupon", {"cart_id": cid, "code": "SAVE10"}))
assert r.status == 200, r
assert r.body["subtotal_cents"] == 1500, r.body
assert r.body["discount_cents"] == 150, r.body
assert r.body["total_cents"] == 1350, r.body

# cart_summary reflects the discount too
r = app.handle(ApiRequest("cart_summary", {"cart_id": cid}))
assert r.body["total_cents"] == 1350 and r.body["discount_cents"] == 150, r.body

# a fixed coupon larger than the subtotal caps at the subtotal
app.handle(ApiRequest("register_coupon", {"code": "TAKE20", "kind": "fixed", "value": 2000}))
r = app.handle(ApiRequest("apply_coupon", {"cart_id": cid, "code": "TAKE20"}))
assert r.body["discount_cents"] == 1500 and r.body["total_cents"] == 0, r.body

# applying an unknown coupon code -> 404
r = app.handle(ApiRequest("apply_coupon", {"cart_id": cid, "code": "GHOST"}))
assert r.status == 404, r

# registering an out-of-range percent -> 400 (ValidationError mapping)
r = app.handle(ApiRequest("register_coupon", {"code": "BAD", "kind": "percent", "value": 150}))
assert r.status == 400, r

print("HELDOUT_OK")
