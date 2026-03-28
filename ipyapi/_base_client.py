"""Shared base class for ipyapi sync and async clients."""

import ipaddress
from typing import Literal

import httpx

from .exceptions import (
    BadRequestError,
    ForbiddenError,
    InvalidIPAddressError,
    MethodNotAllowedError,
    NotFoundError,
    RateLimitError,
    ReservedIPAddressError,
)
from .models import ErrorResponse

ResponseFormat = Literal["json", "xml", "csv", "yaml", "jsonp"]
FieldName = Literal[
    "ip",
    "network",
    "version",
    "city",
    "region",
    "region_code",
    "country",
    "country_name",
    "country_code",
    "country_code_iso3",
    "country_capital",
    "country_tld",
    "continent_code",
    "in_eu",
    "postal",
    "latitude",
    "longitude",
    "latlong",
    "timezone",
    "utc_offset",
    "country_calling_code",
    "currency",
    "currency_name",
    "languages",
    "country_area",
    "country_population",
    "asn",
    "org",
]


class _BaseIPyAPI:
    """Shared base for IPyAPI and AsyncIPyAPI. Not intended for direct use."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://ipapi.co",
        timeout: float = 10.0,
        max_retries: int = 3,
        retry_backoff: float = 1.0,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._timeout = timeout
        self._max_retries = max_retries
        self._retry_backoff = retry_backoff

    def _build_endpoint(self, ip: str | None, suffix: str) -> str:
        """Build the URL path for a request."""
        if ip:
            return f"{ip}/{suffix}/"
        return f"{suffix}/"

    def _validate_ip(self, ip: str) -> None:
        """Validate IP address format. Raises InvalidIPAddressError if invalid."""
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            raise InvalidIPAddressError(ip)

    def _handle_error_response(self, response: httpx.Response) -> None:
        """Raise the appropriate exception for a non-200 response."""
        match response.status_code:
            case 400:
                try:
                    error_data = response.json()
                    if isinstance(error_data, dict) and error_data.get("error"):
                        error = ErrorResponse.from_dict(error_data)
                        if "Invalid IP" in error.reason:
                            raise InvalidIPAddressError(error.message)
                        elif "Reserved IP" in error.reason:
                            raise ReservedIPAddressError(error.message)
                        raise BadRequestError(error.message)
                except ValueError:
                    pass
                raise BadRequestError("Bad Request")
            case 403:
                raise ForbiddenError()
            case 404:
                raise NotFoundError()
            case 405:
                raise MethodNotAllowedError()
            case 429:
                raise RateLimitError()
            case _:
                response.raise_for_status()
