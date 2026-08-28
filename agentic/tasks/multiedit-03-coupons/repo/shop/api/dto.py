"""Request/response envelopes used by the API layer.

The API is transport-agnostic: an ApiRequest carries an `action` string plus a `params`
dict, and the App returns an ApiResponse with a `status` and a JSON-able `body`.
"""


class ApiRequest:
    def __init__(self, action, params=None):
        self.action = action
        self.params = params or {}


class ApiResponse:
    def __init__(self, status, body):
        self.status = status
        self.body = body

    def ok(self):
        return 200 <= self.status < 300

    def __repr__(self):
        return "ApiResponse(status=%d, body=%r)" % (self.status, self.body)
