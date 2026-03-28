"""Asynchronous client for ipapi.co API."""

import asyncio
from typing import Any, Literal, overload

import httpx

from ._base_client import FieldName, ResponseFormat, _BaseIPyAPI
from .exceptions import RateLimitError
from .models import _PYDANTIC_AVAILABLE, IPLocation, PydanticIPLocation
from .types import ReturnType


class AsyncIPyAPI(_BaseIPyAPI):
    """Asynchronous client for ipapi.co IP geolocation API.

    Example:
        >>> async with AsyncIPyAPI() as client:
        ...     location = await client.get_location("8.8.8.8")
        ...     print(location.country_name)
        United States
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://ipapi.co",
        timeout: float = 10.0,
        max_retries: int = 3,
        retry_backoff: float = 1.0,
    ) -> None:
        """Initialize the AsyncIPyAPI client.

        Args:
            api_key: Optional API key for authenticated requests (paid plans).
            base_url: Base URL for the API (default: https://ipapi.co).
            timeout: Request timeout in seconds (default: 10.0).
            max_retries: Number of retries on 429 Rate Limit (default: 3).
            retry_backoff: Base backoff in seconds; sleeps backoff * 2^attempt (default: 1.0).
        """
        super().__init__(api_key, base_url, timeout, max_retries, retry_backoff)
        self._client = httpx.AsyncClient(timeout=timeout)

    async def __aenter__(self) -> "AsyncIPyAPI":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    async def _request(self, endpoint: str) -> httpx.Response:
        url = f"{self._base_url}/{endpoint}"
        params = {"key": self._api_key} if self._api_key else None

        for attempt in range(self._max_retries + 1):
            response = await self._client.get(url, params=params)
            if response.status_code == 429 and attempt < self._max_retries:
                await asyncio.sleep(self._retry_backoff * (2**attempt))
                continue
            if response.status_code != 200:
                self._handle_error_response(response)
            return response

        raise RateLimitError()  # unreachable; satisfies type checker

    @overload
    async def get_location(
        self, ip_address: str | None = None, return_type: Literal[ReturnType.OBJECT] = ...
    ) -> IPLocation: ...

    @overload
    async def get_location(
        self, ip_address: str | None, return_type: Literal[ReturnType.DICT]
    ) -> dict[str, Any]: ...

    @overload
    async def get_location(
        self, ip_address: str | None, return_type: Literal[ReturnType.PYDANTIC]
    ) -> Any: ...

    async def get_location(
        self,
        ip_address: str | None = None,
        return_type: ReturnType = ReturnType.OBJECT,
    ) -> IPLocation | dict[str, Any] | Any:
        """Get complete location information for an IP address.

        Args:
            ip_address: IP address to lookup. If None, uses client's IP.
            return_type: Return as ReturnType.OBJECT (IPLocation), ReturnType.DICT, or
                ReturnType.PYDANTIC (requires pydantic extra).
        """
        if ip_address:
            self._validate_ip(ip_address)
        response = await self._request(self._build_endpoint(ip_address, "json"))
        data = response.json()
        match return_type:
            case ReturnType.DICT:
                return data
            case ReturnType.PYDANTIC:
                if not _PYDANTIC_AVAILABLE:
                    raise ImportError(
                        "Pydantic is required for ReturnType.PYDANTIC. "
                        "Install it with: pip install 'ipyapi[pydantic]' or uv add ipyapi[pydantic]"
                    )
                return PydanticIPLocation.model_validate(data)
            case _:
                return IPLocation.from_dict(data)

    async def get_field(self, field: FieldName, ip_address: str | None = None) -> str:
        """Get a single field for an IP address."""
        if ip_address:
            self._validate_ip(ip_address)
        response = await self._request(self._build_endpoint(ip_address, field))
        return response.text.strip()

    async def get_location_raw(
        self, ip_address: str | None = None, format: ResponseFormat = "json"
    ) -> str:
        """Get location information in specified format as raw string."""
        if ip_address:
            self._validate_ip(ip_address)
        response = await self._request(self._build_endpoint(ip_address, format))
        return response.text

    @overload
    async def get_batch(
        self, ip_addresses: list[str], return_type: Literal[ReturnType.OBJECT] = ...
    ) -> list[IPLocation]: ...

    @overload
    async def get_batch(
        self, ip_addresses: list[str], return_type: Literal[ReturnType.DICT]
    ) -> list[dict[str, Any]]: ...

    @overload
    async def get_batch(
        self, ip_addresses: list[str], return_type: Literal[ReturnType.PYDANTIC]
    ) -> list[Any]: ...

    async def get_batch(
        self,
        ip_addresses: list[str],
        return_type: ReturnType = ReturnType.OBJECT,
    ) -> list[IPLocation] | list[dict[str, Any]] | list[Any]:
        """Look up multiple IP addresses concurrently.

        Args:
            ip_addresses: List of IP addresses to look up.
            return_type: Return each result as ReturnType.OBJECT (IPLocation), ReturnType.DICT,
                or ReturnType.PYDANTIC.

        Returns:
            List of results (order matches input, preserved by asyncio.gather).
        """
        results = await asyncio.gather(
            *[self.get_location(ip, return_type=return_type) for ip in ip_addresses]  # type: ignore[call-overload]
        )
        return list(results)  # type: ignore[return-value]

    # Convenience methods
    async def get_ip(self) -> str:
        """Get client's public IP address."""
        return await self.get_field("ip")

    async def get_city(self, ip_address: str | None = None) -> str:
        """Get city for an IP address."""
        return await self.get_field("city", ip_address)

    async def get_country(self, ip_address: str | None = None) -> str:
        """Get country code (e.g. 'US') for an IP address."""
        return await self.get_field("country", ip_address)

    async def get_country_name(self, ip_address: str | None = None) -> str:
        """Get country name (e.g. 'United States') for an IP address."""
        return await self.get_field("country_name", ip_address)

    async def get_timezone(self, ip_address: str | None = None) -> str:
        """Get IANA timezone identifier for an IP address."""
        return await self.get_field("timezone", ip_address)

    async def get_currency(self, ip_address: str | None = None) -> str:
        """Get ISO 4217 currency code for an IP address."""
        return await self.get_field("currency", ip_address)

    async def get_asn(self, ip_address: str | None = None) -> str:
        """Get ASN for an IP address."""
        return await self.get_field("asn", ip_address)

    async def get_org(self, ip_address: str | None = None) -> str:
        """Get organization name for an IP address."""
        return await self.get_field("org", ip_address)
