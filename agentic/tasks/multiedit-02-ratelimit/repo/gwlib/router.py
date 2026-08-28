"""Route registry: maps route names to handler callables."""
from .errors import UnknownRoute


class Router:
    def __init__(self):
        self._routes = {}

    def register(self, route, handler):
        """Register `handler` (a callable taking a Request, returning a body) for `route`."""
        if not callable(handler):
            raise TypeError("handler must be callable")
        self._routes[route] = handler

    def has(self, route):
        return route in self._routes

    def resolve(self, route):
        """Return the handler for `route` or raise UnknownRoute."""
        try:
            return self._routes[route]
        except KeyError:
            raise UnknownRoute(route)

    def routes(self):
        return sorted(self._routes)
