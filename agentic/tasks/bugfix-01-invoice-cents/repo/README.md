# invoicelib

A tiny invoicing library.

- `invoicelib/money.py` — dollar/cent conversion helpers
- `invoicelib/invoice.py` — `Invoice` / `LineItem`
- `tests/test_smoke.py` — smoke test (`python3 tests/test_smoke.py`)

## Known issue
Customers occasionally report that invoice totals are off by a cent on certain
prices (e.g. items priced at $0.70 or $1.15). Totals should be exact to the cent.
