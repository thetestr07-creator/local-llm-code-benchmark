"""configkit — layered configuration loader.

Public API:
    load_config(sources)  -> resolved config dict
    Resolver              -> lower-level multi-source resolver

Sources are merged by ascending priority: later/higher-priority sources
override earlier ones, but nested mappings are *combined*, not replaced.
"""
from .resolver import Resolver, load_config

__all__ = ["Resolver", "load_config"]
