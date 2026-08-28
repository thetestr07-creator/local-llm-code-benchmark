# miniledger

A tiny double-entry bookkeeping library.

- `ledger/models.py`   — `Account`, `Entry`, `Transaction` data models.
- `ledger/posting.py`  — validates and posts balanced transactions.
- `ledger/balances.py` — computes account balances from posted entries.
- `ledger/reconcile.py`— builds a running-balance statement for one account.
- `ledger/report.py`   — trial-balance and summary reporting.
- `ledger/money.py`    — integer-cent money helpers (no floats).

All amounts are integer cents. Debits are positive, credits are negative, and a
valid transaction's entries must sum to zero.
