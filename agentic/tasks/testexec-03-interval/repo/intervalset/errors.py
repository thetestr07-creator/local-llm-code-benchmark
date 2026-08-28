"""Exception types for intervalset. (Currently the public API ignores empty
intervals rather than raising, but this is here for downstream callers.)"""


class IntervalError(ValueError):
    """Base class for interval-related errors."""


class DegenerateInterval(IntervalError):
    """Raised by strict helpers when start >= end and that is not allowed."""
