"""The Gateway ties the router, metrics and clock together and dispatches requests."""
from .router import Router
from .metrics import Metrics
from .clock import SystemClock
from .errors import UnknownRoute, HandlerError


class Gateway:
    def __init__(self, router=None, metrics=None, clock=None):
        self.router = router or Router()
        self.metrics = metrics or Metrics()
        self.clock = clock or SystemClock()

    def register(self, route, handler):
        """Convenience: register a handler on the underlying router."""
        self.router.register(route, handler)

    def dispatch(self, request):
        """Dispatch `request` to its handler and return a Response.

        - Unknown route            -> Response(status=404, ...) and metric "route.unknown".
        - Handler raises            -> Response(status=500, ...) and metric "route.error".
        - Success                  -> Response(status=200, body=<handler result>) and
                                      metric "route.ok".
        Every dispatch also increments the metric "route.<name>.calls".
        """
        self.metrics.incr("route.%s.calls" % request.route)
        try:
            handler = self.router.resolve(request.route)
        except UnknownRoute:
            self.metrics.incr("route.unknown")
            return Response(404, "unknown route: %s" % request.route)
        try:
            body = handler(request)
        except Exception as exc:  # noqa: BLE001 - gateway boundary
            self.metrics.incr("route.error")
            return Response(500, str(HandlerError(request.route, exc)))
        self.metrics.incr("route.ok")
        return Response(200, body)


from .request import Response  # noqa: E402  (placed last to avoid an import cycle)
