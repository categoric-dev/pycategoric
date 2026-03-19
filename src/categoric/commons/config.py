"""Configuration and environment variable helpers."""

import os
from typing import Optional, Type, TypeVar

T = TypeVar("T")


def get_env(
    key: str, default: Optional[str] = None, required: bool = False
) -> Optional[str]:
    """
    Get an environment variable with optional default and required check.

    Args:
        key: Environment variable name
        default: Default value if not found
        required: If True, raises ValueError if not found

    Returns:
        Environment variable value or default

    Raises:
        ValueError: If required=True and variable not found
    """
    value = os.environ.get(key, default)
    if required and value is None:
        raise ValueError(f"Required environment variable '{key}' not found")
    return value


def get_env_bool(key: str, default: bool = False) -> bool:
    """Parse environment variable as boolean."""
    value = os.environ.get(key, "").lower()
    if value in ("1", "true", "yes", "on"):
        return True
    if value in ("0", "false", "no", "off"):
        return False
    return default


def get_env_int(key: str, default: int = 0) -> int:
    """Parse environment variable as integer."""
    try:
        value = os.environ.get(key)
        return int(value) if value is not None else default
    except ValueError, TypeError:
        return default


def get_env_float(key: str, default: float = 0.0) -> float:
    """Parse environment variable as float."""
    try:
        value = os.environ.get(key)
        return float(value) if value is not None else default
    except ValueError, TypeError:
        return default


class ConfigBase:
    """Base class for configuration objects."""

    @classmethod
    def from_env(cls: Type[T], prefix: str = "") -> T:
        """Create config object from environment variables."""
        # This can be overridden in subclasses for custom behavior
        kwargs = {}
        for key, default in cls.__dict__.items():
            if not key.startswith("_"):
                env_key = f"{prefix}{key}".upper() if prefix else key.upper()
                value = get_env(env_key, str(default) if default is not None else None)
                if value is not None:
                    kwargs[key] = value
        return cls(**kwargs)
