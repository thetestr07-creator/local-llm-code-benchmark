"""Integer-cent money helpers. No floats anywhere in the money path."""


def cents_from_str(s):
    """Parse a decimal money string like '12.34' or '-0.05' into integer cents.

    Accepts an optional leading '-', requires at most two fractional digits.
    """
    s = s.strip()
    neg = s.startswith("-")
    if neg:
        s = s[1:]
    if "." in s:
        whole, frac = s.split(".", 1)
    else:
        whole, frac = s, ""
    if len(frac) > 2:
        raise ValueError("too many fractional digits: %r" % s)
    frac = (frac + "00")[:2]
    whole = whole or "0"
    value = int(whole) * 100 + int(frac)
    return -value if neg else value


def format_cents(cents):
    """Render integer cents as a signed decimal string, e.g. -5 -> '-0.05'."""
    neg = cents < 0
    cents = abs(cents)
    text = "%d.%02d" % (cents // 100, cents % 100)
    return "-" + text if neg else text


def add_cents(*values):
    """Sum any number of integer-cent values."""
    total = 0
    for v in values:
        total += int(v)
    return total
