"""Aggregate account balances from a posted journal."""


def account_balance(journal, account_code):
    """Sum every entry in the journal that touches `account_code`.

    Returns integer cents (positive = net debit, negative = net credit).
    """
    total = 0
    for txn in journal:
        for e in txn.entries:
            if e.account_code == account_code:
                total += e.amount_cents
    return total


def all_balances(journal):
    """Return {account_code: balance_cents} across the whole journal."""
    balances = {}
    for txn in journal:
        for e in txn.entries:
            balances[e.account_code] = balances.get(e.account_code, 0) + e.amount_cents
    return balances
