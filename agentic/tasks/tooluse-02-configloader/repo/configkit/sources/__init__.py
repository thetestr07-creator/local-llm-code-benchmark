"""Config sources. Each source exposes `.load()` returning a plain dict and a
`.priority` used to order layers (higher priority wins on conflict)."""
from .defaults import DefaultsSource
from .file import DictFileSource
from .env import EnvSource

__all__ = ["DefaultsSource", "DictFileSource", "EnvSource"]
