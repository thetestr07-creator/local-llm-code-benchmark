"""Billing periods built on top of the inclusive date range utilities.

A BillingPeriod covers every day from start through end (both inclusive), which
matters for proration: a customer billed for March 1 through March 31 is billed
for 31 days, not 30.
"""
from .core import parse_date, date_range, days_in_range


class BillingPeriod:
    def __init__(self, start, end):
        self.start = parse_date(start)
        self.end = parse_date(end)
        if self.end < self.start:
            raise ValueError("end before start")

    def days(self):
        """Number of billable days in this period (inclusive of both ends)."""
        return days_in_range(self.start, self.end)

    def contains(self, day):
        """True if `day` falls within the period (inclusive of both ends)."""
        day = parse_date(day)
        return self.start <= day <= self.end

    def daily_dates(self):
        """Every billable date in the period, in order."""
        return date_range(self.start, self.end)

    def prorate(self, monthly_amount_cents, days_in_month):
        """Amount owed for this period given a monthly rate, in integer cents.

        Charges `monthly_amount_cents` * (billable days / days_in_month), rounded
        to the nearest cent.
        """
        billable = self.days()
        raw = monthly_amount_cents * billable
        # round half up to nearest cent
        return (raw + days_in_month // 2) // days_in_month
