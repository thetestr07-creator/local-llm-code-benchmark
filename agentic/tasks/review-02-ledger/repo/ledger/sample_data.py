"""A small chart of accounts and a few example transactions."""
from .models import Account, Entry, Transaction

CHART = {
    "1000": Account("1000", "Cash", "asset"),
    "1200": Account("1200", "Accounts Receivable", "asset"),
    "4000": Account("4000", "Sales Income", "income"),
    "5000": Account("5000", "Rent Expense", "expense"),
}


def sample_journal():
    """Return a list of balanced transactions using the CHART accounts."""
    return [
        Transaction("t1", "2026-01-02",
                    [Entry("1000", 50000), Entry("4000", -50000)], "cash sale"),
        Transaction("t2", "2026-01-05",
                    [Entry("5000", 20000), Entry("1000", -20000)], "paid rent"),
        Transaction("t3", "2026-01-09",
                    [Entry("1200", 30000), Entry("4000", -30000)], "invoice raised"),
        Transaction("t4", "2026-01-15",
                    [Entry("1000", 30000), Entry("1200", -30000)], "invoice paid"),
    ]
