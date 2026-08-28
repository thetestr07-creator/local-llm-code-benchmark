"""Money parsing and formatting over whole integer cents.

These two functions are stubs — implement them so the tests pass. See prompt.md
for the full specification (signs, currency symbol, grouping, rounding rules).
"""


def parse_amount(s):
    """Parse a human-typed money string into a signed integer number of cents.

    Returns an ``int``. Raises ``ValueError`` on malformed input. See prompt.md.
    """
    raise NotImplementedError


def format_cents(cents, symbol="$", grouping=True):
    """Render a signed integer number of cents as a display string.

    Returns a ``str``. Raises ``TypeError`` if ``cents`` is not an ``int``.
    See prompt.md.
    """
    raise NotImplementedError
