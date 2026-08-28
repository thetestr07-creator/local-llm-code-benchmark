# Code review: find the logic bug in miniledger

`miniledger` is a small double-entry bookkeeping library (see `README.md`). All
amounts are integer cents; debits are positive, credits are negative, and every
valid transaction's entries sum to zero.

Exactly ONE function in this repository has a **logic/correctness bug**: it
computes the wrong result. Every other function is correct. Read the code
(start with `ledger/`) and identify the single buggy function.

The shipped tests in `tests/` all pass — the bug is in behaviour those tests do
not fully pin down, so you must find it by reading, not by running the suite.

## What to produce

Do NOT fix the code. Do NOT modify any file under `ledger/`. Instead, write a
file named `findings.json` at the repository root with EXACTLY this shape:

```json
{"buggy_function": "<function_name>"}
```

`<function_name>` must be one of these exact strings (the reviewable functions
in this library):

- `cents_from_str`
- `format_cents`
- `add_cents`
- `is_balanced`
- `post_transaction`
- `account_balance`
- `all_balances`
- `running_balance`
- `trial_balance`
- `is_trial_balanced`

Use the plain function name only (no module prefix, no parentheses). Write
`findings.json` and then finish.
