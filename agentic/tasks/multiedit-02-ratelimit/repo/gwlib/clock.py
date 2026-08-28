"""A tiny injectable clock so time-dependent logic stays deterministic in tests.

Production code uses `SystemClock`; tests use `ManualClock` and advance it by hand.
Both expose a single method: `now()` returning a float number of seconds.
"""
import time


class SystemClock:
    """Wall-clock time in seconds."""

    def now(self):
        return time.time()


class ManualClock:
    """A clock whose value only changes when you call `advance`."""

    def __init__(self, start=0.0):
        self._t = float(start)

    def now(self):
        return self._t

    def advance(self, seconds):
        """Move the clock forward by `seconds` (must be >= 0)."""
        if seconds < 0:
            raise ValueError("cannot advance the clock backwards")
        self._t += float(seconds)
        return self._t
