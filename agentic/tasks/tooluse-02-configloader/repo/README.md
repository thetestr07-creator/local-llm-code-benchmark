# configkit

Layered configuration loader. Combine several config **sources** — built-in
defaults, a parsed config file, and environment variables — into one effective
configuration.

Sources are ordered by priority (ascending). Higher-priority sources override
lower ones, but **nested sections are combined**: if the file layer sets
`db.host` and an environment variable sets `db.port`, the resolved config keeps
*both*.

```python
from configkit import load_config
from configkit.sources import DefaultsSource, DictFileSource, EnvSource

cfg = load_config([
    DefaultsSource({"db": {"host": "localhost", "port": 5432}}),
    EnvSource({"APP__DB__PORT": "6000"}, prefix="APP"),
])
# cfg == {"db": {"host": "localhost", "port": 6000}}
```

Layout:

- `configkit/resolver.py`  — orders sources and resolves them
- `configkit/sources/`     — `defaults`, `file`, `env`
- `configkit/parser.py`    — tiny INI parser
- `configkit/schema.py` / `validate.py` — optional shape checking
- `configkit/util/`        — merge / flatten / coerce helpers

Run the smoke test with `python3 tests/test_smoke.py`.
