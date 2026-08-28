"""The request/response value objects passed through the gateway."""


class Request:
    """An inbound request.

    Attributes:
        route:  the name of the route to dispatch to (str)
        client: an identifier for the caller (str), used for per-client concerns
        payload: an arbitrary dict of request data
    """

    def __init__(self, route, client="anonymous", payload=None):
        self.route = route
        self.client = client
        self.payload = payload or {}

    def __repr__(self):
        return "Request(route=%r, client=%r)" % (self.route, self.client)


class Response:
    """The result of dispatching a request.

    Attributes:
        status: an integer status code (200 = ok)
        body:   an arbitrary value produced by the handler (or an error message)
    """

    def __init__(self, status, body):
        self.status = status
        self.body = body

    def __repr__(self):
        return "Response(status=%d, body=%r)" % (self.status, self.body)

    def ok(self):
        return self.status == 200
