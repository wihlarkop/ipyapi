"""Tests for asynchronous client."""

import pytest
from pytest_httpx import HTTPXMock

from ipyapi import AsyncIPyAPI
from ipyapi.exceptions import (
    BadRequestError,
    InvalidIPAddressError,
    RateLimitError,
    ReservedIPAddressError,
)
from ipyapi.models import IPLocation


@pytest.fixture
def sample_response():
    """Sample API response data."""
    return {
        "ip": "8.8.8.8",
        "network": "8.8.8.0/24",
        "version": "IPv4",
        "city": "Mountain View",
        "region": "California",
        "region_code": "CA",
        "country": "US",
        "country_name": "United States",
        "country_code": "US",
        "country_code_iso3": "USA",
        "country_capital": "Washington",
        "country_tld": ".us",
        "continent_code": "NA",
        "in_eu": False,
        "postal": "94035",
        "latitude": 37.386,
        "longitude": -122.0838,
        "timezone": "America/Los_Angeles",
        "utc_offset": "-0800",
        "country_calling_code": "+1",
        "currency": "USD",
        "currency_name": "Dollar",
        "languages": "en-US,es-US,haw,fr",
        "country_area": 9629091.0,
        "country_population": 327167434,
        "asn": "AS15169",
        "org": "Google LLC",
    }


@pytest.mark.asyncio
async def test_async_client_initialization():
    """Test async client initialization."""
    client = AsyncIPyAPI()
    assert client._base_url == "https://ipapi.co"
    await client.close()


@pytest.mark.asyncio
async def test_async_client_context_manager():
    """Test async client as context manager."""
    async with AsyncIPyAPI() as client:
        assert client._base_url == "https://ipapi.co"


@pytest.mark.asyncio
async def test_get_location_with_ip(httpx_mock: HTTPXMock, sample_response):
    """Test get_location with specific IP address."""
    httpx_mock.add_response(url="https://ipapi.co/8.8.8.8/json/", json=sample_response)

    async with AsyncIPyAPI() as client:
        location = await client.get_location("8.8.8.8")
        assert isinstance(location, IPLocation)
        assert location.ip == "8.8.8.8"
        assert location.city == "Mountain View"
        assert location.country_name == "United States"
        assert location.latitude == 37.386
        assert location.longitude == -122.0838


@pytest.mark.asyncio
async def test_get_location_dict_return(httpx_mock: HTTPXMock, sample_response):
    """Test get_location returning dict."""
    httpx_mock.add_response(url="https://ipapi.co/8.8.8.8/json/", json=sample_response)

    async with AsyncIPyAPI() as client:
        location = await client.get_location("8.8.8.8", return_type="dict")
        assert isinstance(location, dict)
        assert location["ip"] == "8.8.8.8"
        assert location["city"] == "Mountain View"


@pytest.mark.asyncio
async def test_get_location_client_ip(httpx_mock: HTTPXMock, sample_response):
    """Test get_location without IP address (client IP)."""
    httpx_mock.add_response(url="https://ipapi.co/json/", json=sample_response)

    async with AsyncIPyAPI() as client:
        location = await client.get_location()
        assert isinstance(location, IPLocation)
        assert location.ip == "8.8.8.8"


@pytest.mark.asyncio
async def test_get_field(httpx_mock: HTTPXMock):
    """Test get_field method."""
    httpx_mock.add_response(url="https://ipapi.co/8.8.8.8/country/", text="US")

    async with AsyncIPyAPI() as client:
        country = await client.get_field("country", "8.8.8.8")
        assert country == "US"


@pytest.mark.asyncio
async def test_get_field_client_ip(httpx_mock: HTTPXMock):
    """Test get_field without IP address."""
    httpx_mock.add_response(url="https://ipapi.co/country/", text="US")

    async with AsyncIPyAPI() as client:
        country = await client.get_field("country")
        assert country == "US"


@pytest.mark.asyncio
async def test_get_location_raw_json(httpx_mock: HTTPXMock, sample_response):
    """Test get_location_raw with JSON format."""
    import json

    httpx_mock.add_response(url="https://ipapi.co/8.8.8.8/json/", text=json.dumps(sample_response))

    async with AsyncIPyAPI() as client:
        raw_data = await client.get_location_raw("8.8.8.8", format="json")
        assert "8.8.8.8" in raw_data
        assert "Mountain View" in raw_data


@pytest.mark.asyncio
async def test_get_location_raw_xml(httpx_mock: HTTPXMock):
    """Test get_location_raw with XML format."""
    xml_response = '<?xml version="1.0" encoding="UTF-8"?><ip>8.8.8.8</ip>'
    httpx_mock.add_response(url="https://ipapi.co/8.8.8.8/xml/", text=xml_response)

    async with AsyncIPyAPI() as client:
        raw_data = await client.get_location_raw("8.8.8.8", format="xml")
        assert "<?xml" in raw_data
        assert "8.8.8.8" in raw_data


@pytest.mark.asyncio
async def test_get_location_raw_csv(httpx_mock: HTTPXMock):
    """Test get_location_raw with CSV format."""
    csv_response = "ip,city,country\n8.8.8.8,Mountain View,US"
    httpx_mock.add_response(url="https://ipapi.co/8.8.8.8/csv/", text=csv_response)

    async with AsyncIPyAPI() as client:
        raw_data = await client.get_location_raw("8.8.8.8", format="csv")
        assert "8.8.8.8" in raw_data
        assert "Mountain View" in raw_data


@pytest.mark.asyncio
async def test_convenience_methods(httpx_mock: HTTPXMock):
    """Test convenience methods for specific fields."""
    httpx_mock.add_response(url="https://ipapi.co/ip/", text="8.8.8.8")
    httpx_mock.add_response(url="https://ipapi.co/8.8.8.8/city/", text="Mountain View")
    httpx_mock.add_response(url="https://ipapi.co/8.8.8.8/country/", text="US")
    httpx_mock.add_response(url="https://ipapi.co/8.8.8.8/country_name/", text="United States")
    httpx_mock.add_response(url="https://ipapi.co/8.8.8.8/timezone/", text="America/Los_Angeles")
    httpx_mock.add_response(url="https://ipapi.co/8.8.8.8/currency/", text="USD")
    httpx_mock.add_response(url="https://ipapi.co/8.8.8.8/asn/", text="AS15169")
    httpx_mock.add_response(url="https://ipapi.co/8.8.8.8/org/", text="Google LLC")

    async with AsyncIPyAPI() as client:
        assert await client.get_ip() == "8.8.8.8"
        assert await client.get_city("8.8.8.8") == "Mountain View"
        assert await client.get_country("8.8.8.8") == "US"
        assert await client.get_country_name("8.8.8.8") == "United States"
        assert await client.get_timezone("8.8.8.8") == "America/Los_Angeles"
        assert await client.get_currency("8.8.8.8") == "USD"
        assert await client.get_asn("8.8.8.8") == "AS15169"
        assert await client.get_org("8.8.8.8") == "Google LLC"


@pytest.mark.asyncio
async def test_rate_limit_error(httpx_mock: HTTPXMock):
    """Test rate limit error handling."""
    httpx_mock.add_response(url="https://ipapi.co/8.8.8.8/json/", status_code=429)

    async with AsyncIPyAPI() as client:
        with pytest.raises(RateLimitError) as exc_info:
            await client.get_location("8.8.8.8")
        assert exc_info.value.status_code == 429


@pytest.mark.asyncio
async def test_invalid_ip_error(httpx_mock: HTTPXMock):
    """Test invalid IP address error handling."""
    error_response = {
        "error": True,
        "reason": "Invalid IP Address",
        "message": "The provided IP address is invalid",
    }
    httpx_mock.add_response(
        url="https://ipapi.co/invalid/json/", status_code=400, json=error_response
    )

    async with AsyncIPyAPI() as client:
        with pytest.raises(InvalidIPAddressError):
            await client.get_location("invalid")


@pytest.mark.asyncio
async def test_reserved_ip_error(httpx_mock: HTTPXMock):
    """Test reserved IP address error handling."""
    error_response = {
        "error": True,
        "reason": "Reserved IP Address",
        "message": "The provided IP address is reserved",
    }
    httpx_mock.add_response(
        url="https://ipapi.co/127.0.0.1/json/", status_code=400, json=error_response
    )

    async with AsyncIPyAPI() as client:
        with pytest.raises(ReservedIPAddressError):
            await client.get_location("127.0.0.1")


@pytest.mark.asyncio
async def test_bad_request_error(httpx_mock: HTTPXMock):
    """Test generic bad request error handling."""
    httpx_mock.add_response(url="https://ipapi.co/8.8.8.8/json/", status_code=400)

    async with AsyncIPyAPI() as client:
        with pytest.raises(BadRequestError):
            await client.get_location("8.8.8.8")


@pytest.mark.asyncio
async def test_custom_base_url():
    """Test async client with custom base URL."""
    client = AsyncIPyAPI(base_url="https://custom.api.com")
    assert client._base_url == "https://custom.api.com"
    await client.close()


@pytest.mark.asyncio
async def test_custom_timeout():
    """Test async client with custom timeout."""
    client = AsyncIPyAPI(timeout=30.0)
    assert client._client.timeout.read == 30.0
    await client.close()
