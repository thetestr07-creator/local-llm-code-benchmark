Add **coupon codes** to the `shop` application. A coupon reduces a cart's total. The feature
must be threaded through every layer: model, store, service, and api.

Prices are always **integer cents**. Read the existing code first (`shop/errors.py`,
`shop/model/cart.py`, `shop/service/cart_service.py`, `shop/api/app.py`, `shop/factory.py`).

## 1. Model — new file `shop/model/coupon.py`

Create a class `Coupon`:

- `Coupon(code, kind, value)`
  - `code`: a non-empty string; raise `ValidationError` if empty/falsy.
  - `kind`: either the string `"percent"` or `"fixed"`; anything else raises `ValidationError`.
  - `value`:
    - for `kind == "percent"`: an integer 0..100 inclusive (the percent off); outside that
      range raises `ValidationError`.
    - for `kind == "fixed"`: a non-negative integer number of **cents** off; negative raises
      `ValidationError`.
- `Coupon.discount_for(subtotal_cents)` returns the integer cents to subtract from a subtotal:
  - percent: `round(subtotal_cents * value / 100)` (nearest cent).
  - fixed: `min(value, subtotal_cents)` (never discount more than the subtotal).
  - The returned discount must never exceed `subtotal_cents` and never be negative.

Import `ValidationError` from `shop.errors`.

## 2. Model — wire the coupon into `shop/model/cart.py`

- `Cart` gains an attribute `coupon` initialised to `None`.
- Add `Cart.apply_coupon(coupon)` which stores the coupon (or `None` to clear it).
- Add `Cart.discount_cents()` returning `0` when there is no coupon, otherwise
  `coupon.discount_for(self.subtotal_cents())`.
- Change `Cart.total_cents()` to return `subtotal_cents() - discount_cents()` (so with no
  coupon it is unchanged).

## 3. Store — new file `shop/store/coupon_store.py`

Create `CouponStore` mirroring the other stores (use `InMemoryCollection` from
`shop.store.base`), keyed by the coupon `code`:
- `save(coupon)` -> stores and returns the coupon (key = `coupon.code`).
- `get(code)` -> returns the coupon or raises `NotFound` (the collection already does this).
- `exists(code)` -> bool.

## 4. Service — wire coupons into `shop/service/cart_service.py`

- `CartService.__init__` gains a **third** parameter `coupon_store` (add it after the existing
  ones; do not reorder `cart_store`, `product_store`). Store it as `self.coupons`.
- Add `CartService.register_coupon(code, kind, value)` that builds a `Coupon`, saves it in the
  coupon store, and returns it.
- Add `CartService.apply_coupon(cart_id, code)`:
  - load the cart (`NotFound` if missing — the store handles this),
  - look up the coupon by `code` (`NotFound` if missing — the store handles this),
  - call `cart.apply_coupon(coupon)`, save the cart, and return the cart.
- Extend `CartService.summary(...)`'s returned dict with a new key `discount_cents`
  (the cart's `discount_cents()`). `total_cents` must now reflect the discount. Keep all the
  existing keys.

## 5. API — wire coupons into `shop/api/app.py` and `shop/factory.py`

- In `factory.build_app()`, construct a `CouponStore` and pass it into `CartService` as the new
  `coupon_store` argument. Nothing else about the wiring changes.
- Register two new actions in `App._routes`:
  - `"register_coupon"` -> params `code`, `kind`, `value`; calls
    `carts.register_coupon(...)` and returns `{"code": <code>, "kind": <kind>, "value": <value>}`.
  - `"apply_coupon"` -> params `cart_id`, `code`; calls `carts.apply_coupon(...)` and returns
    the cart summary (`carts.summary(cart_id)`).
- The existing error mapping already turns `ValidationError`->400 and `NotFound`->404, so
  applying a missing coupon code must yield a 404 and an out-of-range percent must yield a 400.

## Constraints

- Do not change existing public method signatures other than as described (the new
  `coupon_store` parameter on `CartService.__init__`, and the extra `discount_cents` key).
- Keep `python3 tests/test_smoke.py` passing and the library importable.
- Pure standard library only.
