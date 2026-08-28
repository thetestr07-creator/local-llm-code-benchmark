The `invoicelib` package computes invoice totals in integer cents, but customers
report totals are sometimes off by a cent for certain prices (for example items
priced at $0.70 or $1.15). Totals must be exact to the cent for any price given to
two decimal places.

Find and fix the bug so that dollar amounts convert to cents correctly. Do not
change the public function or method signatures (`to_cents`, `cents_to_str`,
`Invoice.add`, `Invoice.total_cents`). Keep the library importable.

You can run the existing smoke test with `python3 tests/test_smoke.py`.
