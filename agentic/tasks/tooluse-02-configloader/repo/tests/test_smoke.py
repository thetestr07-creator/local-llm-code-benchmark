"""Smoke test — passes on the current code. Exercises basic top-level
overriding and the individual source/parser/coercion helpers, but NOT the
partial nested-merge behavior that the bug affects.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from configkit import load_config
from configkit.sources import DefaultsSource, DictFileSource, EnvSource
from configkit.parser import parse_ini
from configkit.util.coerce import coerce_scalar
from configkit.util.flatten import flatten, unflatten

# Top-level scalar override: higher-priority source replaces a scalar.
cfg = load_config([
    DefaultsSource({"debug": False, "name": "base"}),
    DictFileSource({"name": "app"}),
])
assert cfg["debug"] is False
assert cfg["name"] == "app"

# Env source parses namespaced vars into a nested tree.
env = EnvSource({"APP__DB__HOST": "db1", "OTHER": "ignored"}, prefix="APP").load()
assert env == {"db": {"host": "db1"}}

# Parser + helpers behave.
doc = parse_ini("[db]\nhost = localhost\nport = 5432\n")
assert doc == {"db": {"host": "localhost", "port": "5432"}}
assert coerce_scalar("true") is True
assert coerce_scalar("42") == 42
assert unflatten(flatten({"a": {"b": 1}})) == {"a": {"b": 1}}

print("smoke OK")
