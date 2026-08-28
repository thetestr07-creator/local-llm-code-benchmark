"""HELD-OUT verification for review-02-ledger.

The planted bug lives in `running_balance` (ledger/reconcile.py): it does
`running = amt` instead of `running += amt`, so the reported "balance" is just
the current transaction's amount rather than a true running balance, and the
`opening_balance` argument is silently ignored. The model must name
`running_balance`.

This test only inspects the model's verdict file; it does not import the repo.
Pure stdlib. Deterministic.
"""
import os
import json

BUGGY = "running_balance"
ALLOWED = {
    "cents_from_str", "format_cents", "add_cents",
    "is_balanced", "post_transaction",
    "account_balance", "all_balances",
    "running_balance",
    "trial_balance", "is_trial_balanced",
}

repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
findings_path = os.path.join(repo, "findings.json")

if not os.path.exists(findings_path):
    raise AssertionError("findings.json was not created at the repo root")

with open(findings_path, encoding="utf-8") as fh:
    data = json.load(fh)

if not isinstance(data, dict):
    raise AssertionError("findings.json must contain a JSON object, got %r" % type(data).__name__)

name = data.get("buggy_function")

if name not in ALLOWED:
    raise AssertionError(
        "buggy_function %r is not one of the allowed function names %s"
        % (name, sorted(ALLOWED))
    )

if name != BUGGY:
    raise AssertionError("identified %r, expected %r" % (name, BUGGY))

print("HELDOUT_OK")
