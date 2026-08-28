"""Digit-grouping helper. Fully implemented (not a stub).

This inserts thousands separators into a string of decimal digits. You may use
it from core.format_cents, or implement grouping yourself — either is fine.
"""


def group_digits(digits, sep=","):
    """Insert ``sep`` every three digits from the right.

    ``group_digits("1234567")`` -> ``"1,234,567"``. Input must be a string of
    ASCII digits (no sign, no decimal point).
    """
    if not digits.isdigit():
        raise ValueError("group_digits expects a run of decimal digits")
    n = len(digits)
    out = []
    for i, ch in enumerate(digits):
        if i > 0 and (n - i) % 3 == 0:
            out.append(sep)
        out.append(ch)
    return "".join(out)
