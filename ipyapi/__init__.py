"""IPyAPI - Modern Python client for ipapi.co IP geolocation API.

Example usage:
    >>> from ipyapi import IPyAPI
    >>>
    >>> # Synchronous usage
    >>> with IPyAPI() as client:
    ...     location = client.get_location("8.8.8.8")
    ...     print(f"{location.city}, {location.country_name}")
    Mountain View, United States

    >>> # Async usage
    >>> import asyncio
    >>> from ipyapi import AsyncIPyAPI
    >>>
    >>> async def main():
    ...     async with AsyncIPyAPI() as client:
    ...         location = await client.get_location("8.8.8.8")
    ...         print(location.country_name)
    >>> asyncio.run(main())
    United States
"""

from .async_client import AsyncIPyAPI
from .client import IPyAPI
from .exceptions import (
    BadRequestError,
    ForbiddenError,
    InvalidIPAddressError,
    IPyAPIError,
    MethodNotAllowedError,
    NotFoundError,
    RateLimitError,
    ReservedIPAddressError,
)
from .models import ErrorResponse, IPLocation, PydanticIPLocation
from .types import ReturnType

__version__ = "0.2.0"
__all__ = [
    # Clients
    "IPyAPI",
    "AsyncIPyAPI",
    # Models
    "IPLocation",
    "ErrorResponse",
    "PydanticIPLocation",
    # Types
    "ReturnType",
    # Exceptions
    "IPyAPIError",
    "BadRequestError",
    "ForbiddenError",
    "NotFoundError",
    "MethodNotAllowedError",
    "RateLimitError",
    "InvalidIPAddressError",
    "ReservedIPAddressError",
]
