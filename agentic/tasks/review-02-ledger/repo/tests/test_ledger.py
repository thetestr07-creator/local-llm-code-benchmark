"""Project self-tests. Run with:  python -m unittest -v

These exercise the public API. They are the tests shipped with the project; the
grade is decided by separate hidden tests.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ledger.money import cents_from_str, format_cents, add_cents
from ledger.posting import is_balanced, post_transaction, PostingError
from ledger.balances import account_balance, all_balances
from ledger.report import trial_balance, is_trial_balanced
from ledger.reconcile import running_balance
from ledger.models import Transaction, Entry
from ledger.sample_data import CHART, sample_journal


def build_journal():
    journal = []
    for txn in sample_journal():
        post_transaction(journal, txn, CHART)
    return journal


class TestMoney(unittest.TestCase):
    def test_parse_roundtrip(self):
        self.assertEqual(cents_from_str("12.34"), 1234)
        self.assertEqual(cents_from_str("-0.05"), -5)
        self.assertEqual(cents_from_str("100"), 10000)
        self.assertEqual(format_cents(-5), "-0.05")
        self.assertEqual(format_cents(1234), "12.34")

    def test_add(self):
        self.assertEqual(add_cents(100, 200, -50), 250)


class TestPosting(unittest.TestCase):
    def test_balanced(self):
        t = Transaction("x", "2026-01-01", [Entry("1000", 100), Entry("4000", -100)])
        self.assertTrue(is_balanced(t))

    def test_unbalanced_rejected(self):
        t = Transaction("x", "2026-01-01", [Entry("1000", 100), Entry("4000", -90)])
        with self.assertRaises(PostingError):
            post_transaction([], t, CHART)

    def test_unknown_account_rejected(self):
        t = Transaction("x", "2026-01-01", [Entry("9999", 100), Entry("4000", -100)])
        with self.assertRaises(PostingError):
            post_transaction([], t, CHART)


class TestBalances(unittest.TestCase):
    def test_cash_balance(self):
        j = build_journal()
        # 50000 in, 20000 out, 30000 in = 60000
        self.assertEqual(account_balance(j, "1000"), 60000)

    def test_all_balances_sum_to_zero(self):
        j = build_journal()
        self.assertEqual(sum(all_balances(j).values()), 0)


class TestReport(unittest.TestCase):
    def test_trial_balances(self):
        self.assertTrue(is_trial_balanced(build_journal()))


class TestReconcileShape(unittest.TestCase):
    """Structural checks only: line count and the per-line amount field."""

    def test_line_count_and_amounts(self):
        j = build_journal()
        lines = running_balance(j, "1000")
        self.assertEqual([l["txn_id"] for l in lines], ["t1", "t2", "t4"])
        self.assertEqual([l["amount"] for l in lines], [50000, -20000, 30000])


if __name__ == "__main__":
    unittest.main()
