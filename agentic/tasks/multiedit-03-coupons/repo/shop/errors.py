"""Error hierarchy shared across the shop application."""


class ShopError(Exception):
    """Base class for all application errors."""


class NotFound(ShopError):
    """A requested entity does not exist."""


class ValidationError(ShopError):
    """Input failed validation."""


class ConflictError(ShopError):
    """The requested operation conflicts with current state."""
