"""HELD-OUT verification for tooluse-02. The model never sees this."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from configkit import load_config, Resolver
from configkit.sources import DefaultsSource, DictFileSource, EnvSource
from configkit.util.merge import deep_merge, merge_all

# --- direct deep_merge: partial nested override must preserve siblings ---
base = {"db": {"host": "localhost", "port": 5432}}
over = {"db": {"port": 6000}}
assert deep_merge(base, over) == {"db": {"host": "localhost", "port": 6000}}, \
    "deep_merge dropped a sibling key"

# base must not be mutated
assert base == {"db": {"host": "localhost", "port": 5432}}, "deep_merge mutated base"

# --- deep (3-level) nesting ---
b2 = {"db": {"pool": {"size": 5, "timeout": 30}}}
o2 = {"db": {"pool": {"size": 20}}}
assert deep_merge(b2, o2) == {"db": {"pool": {"size": 20, "timeout": 30}}}

# --- merge_all folds an ordered list of layers ---
layers = [
    {"db": {"host": "h0", "port": 1, "pool": {"size": 5, "timeout": 30}}},
    {"db": {"port": 2}},
    {"db": {"pool": {"size": 9}}, "cache": {"ttl": 60}},
]
assert merge_all(layers) == {
    "db": {"host": "h0", "port": 2, "pool": {"size": 9, "timeout": 30}},
    "cache": {"ttl": 60},
}

# --- end-to-end through the public loader, sources ordered by priority ---
cfg = load_config([
    DefaultsSource({"db": {"host": "localhost", "port": 5432, "pool": {"size": 5, "timeout": 30}}}),
    DictFileSource({"db": {"pool": {"size": 10}}}),
    EnvSource({"APP__DB__PORT": "6000"}, prefix="APP"),
])
assert cfg == {
    "db": {"host": "localhost", "port": 6000, "pool": {"size": 10, "timeout": 30}},
}, "end-to-end resolved config lost nested siblings: %r" % (cfg,)

# --- Resolver instance, add order independent of priority ---
r = Resolver()
r.add(EnvSource({"APP__CACHE__TTL": "120"}, prefix="APP"))
r.add(DefaultsSource({"cache": {"backend": "mem", "ttl": 60}}))
assert r.resolve() == {"cache": {"backend": "mem", "ttl": 120}}

print("HELDOUT_OK")
