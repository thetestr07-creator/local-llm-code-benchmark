"""Validation and posting of transactions into an in-memory journal."""


class PostingError(Exception):
    pass


def is_balanced(txn):
    """A transaction is balanced iff its entry amounts sum to exactly zero."""
    total = 0
    for e in txn.entries:
        total += e.amount_cents
    return total == 0


def post_transaction(journal, txn, known_accounts):
    """Append `txn` to `journal` after validating it.

    Rules:
      - the transaction must reference at least two entries,
      - every entry's account must be a known account code,
      - the transaction must be balanced (entries sum to zero).
    Returns the journal (mutated in place).
    """
    if len(txn.entries) < 2:
        raise PostingError("transaction %r needs at least two entries" % txn.txn_id)
    for e in txn.entries:
        if e.account_code not in known_accounts:
            raise PostingError("unknown account %r" % e.account_code)
    if not is_balanced(txn):
        raise PostingError("transaction %r does not balance" % txn.txn_id)
    journal.append(txn)
    return journal
