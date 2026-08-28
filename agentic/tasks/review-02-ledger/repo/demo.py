"""Tiny demo: post the sample journal and print a running statement for Cash."""
from ledger.sample_data import CHART, sample_journal
from ledger.posting import post_transaction
from ledger.reconcile import running_balance
from ledger.money import format_cents


def main():
    journal = []
    for txn in sample_journal():
        post_transaction(journal, txn, CHART)

    print("Cash (1000) statement:")
    for line in running_balance(journal, "1000"):
        print("  %s  amount=%s  balance=%s"
              % (line["txn_id"], format_cents(line["amount"]), format_cents(line["balance"])))


if __name__ == "__main__":
    main()
