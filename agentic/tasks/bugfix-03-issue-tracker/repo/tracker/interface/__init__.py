"""Interface layer: a text command router and a CLI front end."""
from .router import CommandRouter, RouterError

__all__ = ["CommandRouter", "RouterError"]
