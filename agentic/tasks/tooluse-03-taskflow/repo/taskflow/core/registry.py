"""Task registry: map task names to callables.

Applications register plain functions under a name; the engine looks them up
when a Job is executed. This module is intentionally decoupled from retry logic.
"""

_REGISTRY = {}


def register(name, fn=None):
    """Register `fn` under `name`. Usable as a decorator when `fn` is omitted."""
    if fn is None:
        def deco(f):
            _REGISTRY[name] = f
            return f
        return deco
    _REGISTRY[name] = fn
    return fn


def get_task(name):
    if name not in _REGISTRY:
        raise KeyError("no task registered under %r" % name)
    return _REGISTRY[name]


def clear():
    _REGISTRY.clear()


def registered_names():
    return sorted(_REGISTRY)
