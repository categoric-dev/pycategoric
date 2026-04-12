"""Serialization and deserialization utilities."""

import json
from datetime import datetime
from typing import Any

from loguru import logger


class JSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles common types."""

    def default(self, obj: Any) -> Any:
        """Encode special types to JSON-compatible formats."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, bytes):
            return obj.decode("utf-8", errors="replace")
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        return super().default(obj)


def to_json(obj: Any, **kwargs) -> str:
    """Serialize object to JSON string."""
    return json.dumps(obj, cls=JSONEncoder, **kwargs)


def from_json(data: str, **kwargs) -> Any:
    """Deserialize JSON string to Python object."""
    try:
        return json.loads(data, **kwargs)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
        raise


def safe_json_loads(data: str, default: Any | None = None) -> Any:
    """Safely deserialize JSON string with fallback."""
    try:
        return json.loads(data)
    except json.JSONDecodeError, TypeError:
        return default


def to_dict(obj: Any) -> dict[str, Any]:
    """Convert object to dictionary."""
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    if hasattr(obj, "model_dump"):  # Pydantic v2
        return obj.model_dump()
    if hasattr(obj, "dict"):  # Pydantic v1
        return obj.dict()
    return {}
