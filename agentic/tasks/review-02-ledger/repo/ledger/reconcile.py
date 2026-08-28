"""Build a running-balance statement for a single account.

Given a journal and an account, produce a chronologically ordered list of
statement lines. Each line reports the transaction id, the signed amount that
hit this account in that transaction, and the account's running balance
*after* that transaction is applied.

The running balance of line N is: opening_balance + (sum of this account's
amounts across the first N transactions, inclusive).
"""


def _lines_for_account(journal, account_code):
    """Yield (txn, amount_for_account) for every txn that touches the account,
    preserving journal order. A txn with several legs on the same account
    contributes the sum of those legs."""
    for txn in journal:
        amt = 0
        touched = False
        for e in txn.entries:
            if e.account_code == account_code:
                amt += e.amount_cents
                touched = True
        if touched:
            yield txn, amt


def running_balance(journal, account_code, opening_balance=0):
    """Return a list of dicts: one per transaction touching `account_code`.

    Each dict is {"txn_id", "date", "amount", "balance"} where "balance" is the
    running balance *after* applying that transaction.
    """
    statement = []
    running = opening_balance
    for txn, amt in _lines_for_account(journal, account_code):
        running = amt
        statement.append({
            "txn_id": txn.txn_id,
            "date": txn.date,
            "amount": amt,
            "balance": running,
        })
    return statement
