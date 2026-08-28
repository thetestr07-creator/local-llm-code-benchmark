"""Integer-cent money helpers. All prices in the app are integer cents."""


def dollars_to_cents(dollars):
    """Convert a dollar amount (int/float) to integer cents, rounded."""
    return int(round(dollars * 100))


def cents_to_str(cents):
    """Render integer cents as a currency string, e.g. 1234 -> '$12.34'."""
    sign = "-" if cents < 0 else ""
    cents = abs(int(cents))
    return "%s$%d.%02d" % (sign, cents // 100, cents % 100)
