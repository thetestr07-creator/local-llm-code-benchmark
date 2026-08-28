"""A few example handlers used by the demo and smoke tests.

A handler is any callable that takes a Request and returns a body (any value).
"""


def echo(request):
    """Return the request payload unchanged."""
    return request.payload


def ping(request):
    """A trivial health-check handler."""
    return "pong"


def add(request):
    """Add two numbers supplied in the payload as `a` and `b`."""
    return request.payload["a"] + request.payload["b"]
