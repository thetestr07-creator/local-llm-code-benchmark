Add a percentage-discount feature to `invoicelib`.

1. Create a new module `invoicelib/discount.py` with a function
   `apply_discount(cents, percent)` that returns the integer cents remaining after
   applying a `percent` discount, rounded to the nearest cent. `percent` must be a
   number in the inclusive range 0..100; any value outside that range must raise
   `ValueError`.

2. Wire it into `invoicelib/invoice.py`:
   - add a method `Invoice.set_discount(percent)` that stores the discount
     (validating the range, raising `ValueError` if invalid),
   - make `Invoice.total_cents()` return the discounted total (using
     `apply_discount`). With no discount set, totals are unchanged.

Do not change existing public signatures (`Invoice.add`, `to_cents`, `cents_to_str`).
Keep the library importable. You can run `python3 tests/test_smoke.py`.
