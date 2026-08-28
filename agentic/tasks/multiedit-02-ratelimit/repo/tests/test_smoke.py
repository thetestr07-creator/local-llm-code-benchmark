import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gwlib.gateway import Gateway
from gwlib.request import Request
from gwlib.handlers import ping, add

gw = Gateway()
gw.register("ping", ping)
gw.register("add", add)

r = gw.dispatch(Request("ping"))
assert r.ok() and r.body == "pong", r

r = gw.dispatch(Request("add", payload={"a": 2, "b": 3}))
assert r.ok() and r.body == 5, r

r = gw.dispatch(Request("nope"))
assert r.status == 404, r

assert gw.metrics.get("route.ok") == 2
assert gw.metrics.get("route.unknown") == 1
print("smoke OK")
