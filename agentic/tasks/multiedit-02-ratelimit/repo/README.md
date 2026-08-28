# gwlib

A tiny in-process request gateway.

- `gwlib/request.py` — `Request` / `Response` value objects
- `gwlib/router.py` — `Router`, maps route names to handler callables
- `gwlib/gateway.py` — `Gateway`, dispatches a `Request` to its handler
- `gwlib/metrics.py` — `Metrics`, an in-memory counter store
- `gwlib/clock.py` — `SystemClock` / `ManualClock` (injectable time)
- `gwlib/handlers.py` — example handlers (`echo`, `ping`, `add`)
- `gwlib/config.py` — a simple config holder
- `gwlib/errors.py` — exception types
- `tests/test_smoke.py` — smoke test (`python3 tests/test_smoke.py`)

## Example

```python
from gwlib.gateway import Gateway
from gwlib.request import Request
from gwlib.handlers import ping

gw = Gateway()
gw.register("ping", ping)
resp = gw.dispatch(Request("ping"))
assert resp.ok() and resp.body == "pong"
```
