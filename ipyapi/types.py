"""Shared type definitions for ipyapi."""

from enum import Enum


class ReturnType(Enum):
    """Return type for location lookup methods.

    OBJECT  — IPLocation dataclass (default)
    DICT    — plain Python dict
    PYDANTIC — PydanticIPLocation (requires pydantic extra: uv add ipyapi[pydantic])
    """

    OBJECT = "object"
    DICT = "dict"
    PYDANTIC = "pydantic"
