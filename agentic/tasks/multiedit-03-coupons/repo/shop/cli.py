"""A tiny JSON-in/JSON-out CLI wrapper around the App, handy for manual poking.

Usage: echo '{"action":"list_products","params":{}}' | python3 -m shop.cli
"""
import json
import sys

from .factory import build_app
from .api.dto import ApiRequest


def main(argv=None):
    app = build_app()
    raw = sys.stdin.read()
    data = json.loads(raw) if raw.strip() else {}
    req = ApiRequest(data.get("action", ""), data.get("params", {}))
    resp = app.handle(req)
    print(json.dumps({"status": resp.status, "body": resp.body}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
