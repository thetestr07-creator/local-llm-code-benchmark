"""Domain models. All monetary amounts are integer cents.

Sign convention: a debit is a positive amount, a credit is a negative amount.
A well-formed transaction's entries sum to exactly zero.
"""


class Account:
    def __init__(self, code, name, kind="asset"):
        self.code = code
        self.name = name
        self.kind = kind  # asset | liability | equity | income | expense

    def __repr__(self):
        return "Account(%r, %r)" % (self.code, self.name)


class Entry:
    """One leg of a transaction: a signed integer-cent amount against an account."""

    def __init__(self, account_code, amount_cents):
        self.account_code = account_code
        self.amount_cents = int(amount_cents)

    def __repr__(self):
        return "Entry(%r, %d)" % (self.account_code, self.amount_cents)


class Transaction:
    def __init__(self, txn_id, date, entries, memo=""):
        self.txn_id = txn_id
        self.date = date  # ISO "YYYY-MM-DD" string
        self.entries = list(entries)
        self.memo = memo

    def __repr__(self):
        return "Transaction(%r, %s, %d entries)" % (self.txn_id, self.date, len(self.entries))
