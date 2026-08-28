"""Exception types for configkit."""


class ConfigError(Exception):
    """Base class for configuration problems."""


class ValidationError(ConfigError):
    """Raised when a resolved config fails schema validation."""


class SourceError(ConfigError):
    """Raised when a source cannot produce a mapping."""
