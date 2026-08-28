"""Execution middleware.

Middleware wrap a task call with before/after hooks (timing, logging). They
observe execution but must return the wrapped callable's result unchanged and
must not alter retry behavior. Composed left-to-right around the task callable.
"""


def compose(middlewares, fn):
    wrapped = fn
    for mw in reversed(list(middlewares)):
        wrapped = mw(wrapped)
    return wrapped


def timing_middleware(clock):
    """Middleware factory that records elapsed virtual time per call."""
    def factory(fn):
        def inner(*a, **k):
            start = clock.now()
            try:
                return fn(*a, **k)
            finally:
                clock.record_span(clock.now() - start)
        return inner
    return factory
