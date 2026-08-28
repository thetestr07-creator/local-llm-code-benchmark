"""Money helpers for the invoicing library."""


def to_cents(dollars):
    """Convert a dollar amount (float) to an integer number of cents."""
    return int(round(dollars * 100))


def cents_to_str(cents):
    """Render integer cents as a currency string, e.g. 1234 -> '$12.34'."""
    return "$%d.%02d" % (cents // 100, cents % 100)
