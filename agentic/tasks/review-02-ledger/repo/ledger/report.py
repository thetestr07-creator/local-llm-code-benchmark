"""Trial-balance reporting over a posted journal."""
from .balances import all_balances


def trial_balance(journal):
    """Return a sorted list of (account_code, balance_cents) for every account
    that appears in the journal."""
    balances = all_balances(journal)
    return sorted(balances.items())


def is_trial_balanced(journal):
    """The books balance iff every account's balance sums to zero overall.

    Because every posted transaction sums to zero, the grand total across all
    accounts must also be zero.
    """
    total = 0
    for _code, bal in trial_balance(journal):
        total += bal
    return total == 0
