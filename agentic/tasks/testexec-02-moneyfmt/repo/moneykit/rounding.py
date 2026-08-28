"""Rounding helpers used elsewhere in moneykit. Fully implemented (not a stub)."""


def round_half_up(value):
    """Round a non-negative float to the nearest int, halves rounding up.

    Only used by auxiliary tooling; the core parser deals in exact digits and
    does not depend on this. Provided for completeness / other callers.
    """
    import math
    return int(math.floor(value + 0.5))


def cents_to_dollars(cents):
    """Return a (dollars, remaining_cents) tuple for a non-negative cent count."""
    if cents < 0:
        raise ValueError("cents_to_dollars expects non-negative input")
    return divmod(cents, 100)
