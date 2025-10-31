"""Async client for ipapi.co API."""

from typing import Any, Literal

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
from .models import ErrorResponse, IPLocation

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


class AsyncIPyAPI:
    """Asynchronous client for ipapi.co IP geolocation API.

    Example:
        >>> import asyncio
        >>> async def main():
        ...     client = AsyncIPyAPI()
        ...     location = await client.get_location("8.8.8.8")
        ...     print(location.country_name)
        ...     await client.close()
        >>> asyncio.run(main())
        United States

    Or use as async context manager:
        >>> async def main():
        ...     async with AsyncIPyAPI() as client:
        ...         location = await client.get_location("8.8.8.8")
        >>> asyncio.run(main())
    """

    def __init__(
        self, api_key: str | None = None, base_url: str = "https://ipapi.co", timeout: float = 10.0
    ) -> None:
        """Initialize the AsyncIPyAPI client.

        Args:
            api_key: Optional API key for authenticated requests (for paid plans)
            base_url: Base URL for the API (default: https://ipapi.co)
            timeout: Request timeout in seconds (default: 10.0)
        """
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._client = httpx.AsyncClient(timeout=timeout)

    async def __aenter__(self) -> "AsyncIPyAPI":
        """Enter async context manager."""
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Exit async context manager and close client."""
        await self.close()

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    def _handle_error_response(self, response: httpx.Response) -> None:
        """Handle error responses from the API.

        Args:
            response: HTTP response object

        Raises:
            BadRequestError: For 400 status code
            ForbiddenError: For 403 status code
            NotFoundError: For 404 status code
            MethodNotAllowedError: For 405 status code
            RateLimitError: For 429 status code
            InvalidIPAddressError: For invalid IP error
            ReservedIPAddressError: For reserved IP error
        """
        if response.status_code == 400:
            try:
                error_data = response.json()
                if isinstance(error_data, dict) and error_data.get("error"):
                    error = ErrorResponse.from_dict(error_data)
                    if "Invalid IP" in error.reason:
                        raise InvalidIPAddressError(error.message)
                    elif "Reserved IP" in error.reason:
                        raise ReservedIPAddressError(error.message)
                    raise BadRequestError(error.message)
            except (ValueError, KeyError):
                pass
            raise BadRequestError("Bad Request")
        elif response.status_code == 403:
            raise ForbiddenError()
        elif response.status_code == 404:
            raise NotFoundError()
        elif response.status_code == 405:
            raise MethodNotAllowedError()
        elif response.status_code == 429:
            raise RateLimitError()

        # For other errors, use default raise_for_status
        response.raise_for_status()

    async def _request(self, endpoint: str) -> httpx.Response:
        """Make an async request to the API.

        Args:
            endpoint: API endpoint path

        Returns:
            HTTP response object

        Raises:
            Various IPyAPIError subclasses depending on error type
        """
        url = f"{self._base_url}/{endpoint}"
        params = {"key": self._api_key} if self._api_key else None
        response = await self._client.get(url, params=params)

        if response.status_code != 200:
            self._handle_error_response(response)

        return response

    async def get_location(
        self, ip_address: str | None = None, return_type: Literal["dict", "object"] = "object"
    ) -> IPLocation | dict[str, Any]:
        """Get complete location information for an IP address.

        Args:
            ip_address: IP address to lookup. If None, uses client's IP.
            return_type: Return as 'dict' or 'object' (IPLocation dataclass)

        Returns:
            Location information as IPLocation object or dictionary

        Raises:
            InvalidIPAddressError: If IP address is invalid
            ReservedIPAddressError: If IP address is reserved
            RateLimitError: If rate limit is exceeded
            Other IPyAPIError subclasses for various errors

        Example:
            >>> async def main():
            ...     client = AsyncIPyAPI()
            ...     location = await client.get_location("8.8.8.8")
            ...     print(f"{location.city}, {location.country_name}")
            ...     await client.close()
        """
        if ip_address:
            endpoint = f"{ip_address}/json/"
        else:
            endpoint = "json/"

        response = await self._request(endpoint)
        data = response.json()

        if return_type == "dict":
            return data
        return IPLocation.from_dict(data)

    async def get_field(self, field: FieldName, ip_address: str | None = None) -> str:
        """Get a single field for an IP address.

        Args:
            field: Field name to retrieve
            ip_address: IP address to lookup. If None, uses client's IP.

        Returns:
            Field value as string

        Raises:
            InvalidIPAddressError: If IP address is invalid
            ReservedIPAddressError: If IP address is reserved
            RateLimitError: If rate limit is exceeded

        Example:
            >>> async def main():
            ...     client = AsyncIPyAPI()
            ...     country = await client.get_field("country", "8.8.8.8")
            ...     print(country)
            ...     await client.close()
        """
        if ip_address:
            endpoint = f"{ip_address}/{field}/"
        else:
            endpoint = f"{field}/"

        response = await self._request(endpoint)
        return response.text.strip()

    async def get_location_raw(
        self, ip_address: str | None = None, format: ResponseFormat = "json"
    ) -> str:
        """Get location information in specified format as raw string.

        Args:
            ip_address: IP address to lookup. If None, uses client's IP.
            format: Response format (json, xml, csv, yaml, jsonp)

        Returns:
            Raw response string in specified format

        Raises:
            InvalidIPAddressError: If IP address is invalid
            ReservedIPAddressError: If IP address is reserved
            RateLimitError: If rate limit is exceeded

        Example:
            >>> async def main():
            ...     client = AsyncIPyAPI()
            ...     xml_data = await client.get_location_raw("8.8.8.8", format="xml")
            ...     print(xml_data)
            ...     await client.close()
        """
        if ip_address:
            endpoint = f"{ip_address}/{format}/"
        else:
            endpoint = f"{format}/"

        response = await self._request(endpoint)
        return response.text

    # Convenience methods for specific fields
    async def get_ip(self) -> str:
        """Get client's IP address.

        Returns:
            IP address as string

        Example:
            >>> async def main():
            ...     client = AsyncIPyAPI()
            ...     my_ip = await client.get_ip()
            ...     print(my_ip)
            ...     await client.close()
        """
        return await self.get_field("ip")

    async def get_city(self, ip_address: str | None = None) -> str:
        """Get city for IP address.

        Args:
            ip_address: IP address to lookup. If None, uses client's IP.

        Returns:
            City name
        """
        return await self.get_field("city", ip_address)

    async def get_country(self, ip_address: str | None = None) -> str:
        """Get country code for IP address.

        Args:
            ip_address: IP address to lookup. If None, uses client's IP.

        Returns:
            Country code (e.g., 'US')
        """
        return await self.get_field("country", ip_address)

    async def get_country_name(self, ip_address: str | None = None) -> str:
        """Get country name for IP address.

        Args:
            ip_address: IP address to lookup. If None, uses client's IP.

        Returns:
            Country name (e.g., 'United States')
        """
        return await self.get_field("country_name", ip_address)

    async def get_timezone(self, ip_address: str | None = None) -> str:
        """Get timezone for IP address.

        Args:
            ip_address: IP address to lookup. If None, uses client's IP.

        Returns:
            Timezone identifier (e.g., 'America/New_York')
        """
        return await self.get_field("timezone", ip_address)

    async def get_currency(self, ip_address: str | None = None) -> str:
        """Get currency code for IP address.

        Args:
            ip_address: IP address to lookup. If None, uses client's IP.

        Returns:
            Currency code (e.g., 'USD')
        """
        return await self.get_field("currency", ip_address)

    async def get_asn(self, ip_address: str | None = None) -> str:
        """Get ASN for IP address.

        Args:
            ip_address: IP address to lookup. If None, uses client's IP.

        Returns:
            ASN identifier
        """
        return await self.get_field("asn", ip_address)

    async def get_org(self, ip_address: str | None = None) -> str:
        """Get organization for IP address.

        Args:
            ip_address: IP address to lookup. If None, uses client's IP.

        Returns:
            Organization name
        """
        return await self.get_field("org", ip_address)
