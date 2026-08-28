"""Backoff schedule computation.

`compute_delay` returns how many seconds to wait before a given (0-based)
retry attempt, using exponential growth:

    delay = base_delay * (factor ** attempt)

The growth is bounded above by `max_delay` so that, no matter how many times a
job has failed, a single wait never exceeds the configured cap. `base_delay` is
also treated as a floor for the very first retry.
"""


def compute_delay(attempt, base_delay=1.0, factor=2.0, max_delay=60.0):
    """Seconds to wait before retry number `attempt` (attempt 0 == first retry).

    The raw exponential value is capped at `max_delay`.
    """
    if attempt < 0:
        attempt = 0
    raw = base_delay * (factor ** attempt)
    if raw < base_delay:
        raw = base_delay
    return raw


def schedule(max_attempts, base_delay=1.0, factor=2.0, max_delay=60.0):
    """Materialize the full per-attempt delay schedule (handy for previews)."""
    return [compute_delay(a, base_delay, factor, max_delay) for a in range(max_attempts)]
