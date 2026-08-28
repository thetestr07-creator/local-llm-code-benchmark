"""Exception types used across the gateway."""


class GatewayError(Exception):
    """Base class for all gateway errors."""


class UnknownRoute(GatewayError):
    """Raised when a request targets a route with no registered handler."""


class HandlerError(GatewayError):
    """Raised when a handler itself fails; wraps the original exception."""

    def __init__(self, route, original):
        super().__init__("handler for %r failed: %s" % (route, original))
        self.route = route
        self.original = original
