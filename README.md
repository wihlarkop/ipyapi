# IPyAPI

[![Tests](https://github.com/wihlarkop/ipyapi/actions/workflows/test.yml/badge.svg)](https://github.com/wihlarkop/ipyapi/actions/workflows/test.yml)
[![Code Quality](https://github.com/wihlarkop/ipyapi/actions/workflows/lint.yml/badge.svg)](https://github.com/wihlarkop/ipyapi/actions/workflows/lint.yml)
[![PyPI version](https://badge.fury.io/py/ipyapi.svg)](https://badge.fury.io/py/ipyapi)
[![Python versions](https://img.shields.io/pypi/pyversions/ipyapi.svg)](https://pypi.org/project/ipyapi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, feature-complete Python client library for the [ipapi.co](https://ipapi.co) IP geolocation API. Built with `httpx` and full async support.

## Features

- **Complete API Coverage**: All ipapi.co endpoints supported
- **Multiple Response Formats**: JSON, XML, CSV, YAML, JSONP
- **Sync & Async**: Both synchronous and asynchronous clients
- **Type Hints**: Full type annotations for better IDE support
- **Error Handling**: Comprehensive exception handling for all API errors
- **Well Tested**: Extensive test coverage with pytest
- **Modern Python**: Built for Python 3.9+

## Installation

Install using pip:

```bash
pip install ipyapi
```

Install using uv (recommended):

```bash
uv add ipyapi
```

## Quick Start

### Synchronous Usage

```python
from ipyapi import IPyAPI

# Using context manager (recommended)
with IPyAPI() as client:
    # Get complete location data
    location = client.get_location("8.8.8.8")
    print(f"{location.city}, {location.country_name}")
    # Output: Mountain View, United States

    # Get specific field
    country = client.get_country("8.8.8.8")
    print(country)  # Output: US

    # Get your own IP info
    my_location = client.get_location()
    print(my_location.ip)
```

### Asynchronous Usage

```python
import asyncio
from ipyapi import AsyncIPyAPI

async def main():
    async with AsyncIPyAPI() as client:
        # Get complete location data
        location = await client.get_location("8.8.8.8")
        print(f"{location.city}, {location.country_name}")

        # Get specific field
        country = await client.get_country("8.8.8.8")
        print(country)

asyncio.run(main())
```

## Usage Examples

### Get Complete Location Information

```python
from ipyapi import IPyAPI

with IPyAPI() as client:
    location = client.get_location("8.8.8.8")

    # Access all available fields
    print(f"IP: {location.ip}")
    print(f"City: {location.city}")
    print(f"Region: {location.region}")
    print(f"Country: {location.country_name}")
    print(f"Timezone: {location.timezone}")
    print(f"Currency: {location.currency}")
    print(f"ASN: {location.asn}")
    print(f"Organization: {location.org}")
    print(f"Coordinates: {location.latitude}, {location.longitude}")
```

### Get Data as Dictionary

```python
with IPyAPI() as client:
    # Return as dictionary instead of IPLocation object
    data = client.get_location("8.8.8.8", return_type="dict")
    print(data["country_name"])
```

### Get Single Fields

```python
with IPyAPI() as client:
    # Convenience methods for common fields
    ip = client.get_ip()
    city = client.get_city("8.8.8.8")
    country = client.get_country("8.8.8.8")
    country_name = client.get_country_name("8.8.8.8")
    timezone = client.get_timezone("8.8.8.8")
    currency = client.get_currency("8.8.8.8")
    asn = client.get_asn("8.8.8.8")
    org = client.get_org("8.8.8.8")

    # Or use generic get_field method
    postal = client.get_field("postal", "8.8.8.8")
```

### Different Response Formats

```python
with IPyAPI() as client:
    # Get response in different formats
    json_data = client.get_location_raw("8.8.8.8", format="json")
    xml_data = client.get_location_raw("8.8.8.8", format="xml")
    csv_data = client.get_location_raw("8.8.8.8", format="csv")
    yaml_data = client.get_location_raw("8.8.8.8", format="yaml")
```

### Error Handling

```python
from ipyapi import IPyAPI
from ipyapi.exceptions import (
    RateLimitError,
    InvalidIPAddressError,
    ReservedIPAddressError,
    IPyAPIError
)

with IPyAPI() as client:
    try:
        location = client.get_location("invalid-ip")
    except InvalidIPAddressError as e:
        print(f"Invalid IP: {e.message}")
    except ReservedIPAddressError as e:
        print(f"Reserved IP: {e.message}")
    except RateLimitError as e:
        print(f"Rate limited: {e.message}")
    except IPyAPIError as e:
        print(f"API error: {e.message}")
```

### Custom Configuration

```python
# Custom timeout
client = IPyAPI(timeout=30.0)

# Custom base URL (for testing or proxy)
client = IPyAPI(base_url="https://custom.api.url")
```

## API Reference

### IPyAPI / AsyncIPyAPI

Main client classes for interacting with the ipapi.co API.

#### Methods

- `get_location(ip_address=None, return_type="object")` - Get complete location data
- `get_field(field, ip_address=None)` - Get a single field value
- `get_location_raw(ip_address=None, format="json")` - Get raw response in specified format

#### Convenience Methods

- `get_ip()` - Get client's IP address
- `get_city(ip_address=None)` - Get city name
- `get_country(ip_address=None)` - Get country code
- `get_country_name(ip_address=None)` - Get country name
- `get_timezone(ip_address=None)` - Get timezone
- `get_currency(ip_address=None)` - Get currency code
- `get_asn(ip_address=None)` - Get ASN
- `get_org(ip_address=None)` - Get organization name

### IPLocation

Dataclass containing complete IP location information.

**Fields:**
- `ip`, `network`, `version`
- `city`, `region`, `region_code`
- `country`, `country_name`, `country_code`, `country_code_iso3`
- `country_capital`, `country_tld`, `continent_code`
- `in_eu`, `postal`
- `latitude`, `longitude`
- `timezone`, `utc_offset`
- `country_calling_code`
- `currency`, `currency_name`
- `languages`
- `country_area`, `country_population`
- `asn`, `org`
- `hostname` (optional)

### Exceptions

All exceptions inherit from `IPyAPIError`:

- `BadRequestError` - 400 Bad Request
- `ForbiddenError` - 403 Forbidden (Authentication Failed)
- `NotFoundError` - 404 Not Found
- `MethodNotAllowedError` - 405 Method Not Allowed
- `RateLimitError` - 429 Too Many Requests
- `InvalidIPAddressError` - Invalid IP address format
- `ReservedIPAddressError` - Reserved/private IP address

## Development

### Setup with uv

```bash
# Clone the repository
git clone https://github.com/wihlarkop/ipyapi.git
cd ipyapi

# Install with dev dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=ipyapi --cov-report=html
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_client.py

# Run with coverage
uv run pytest --cov=ipyapi --cov-report=term-missing
```

## Rate Limits

The free ipapi.co API has rate limits:
- **Free tier**: 1,000 requests per day
- **No registration**: 30 requests per minute

For higher limits, consider [ipapi.co's paid plans](https://ipapi.co/pricing/).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built on top of the excellent [ipapi.co](https://ipapi.co) API
- Uses [httpx](https://www.python-httpx.org/) for HTTP requests
- Managed with [uv](https://github.com/astral-sh/uv) for fast, reliable package management

## Links

- **Documentation**: [ipapi.co API docs](https://ipapi.co/api/)
- **PyPI**: [pypi.org/project/ipyapi](https://pypi.org/project/ipyapi/)
- **Source Code**: [github.com/wihlarkop/ipyapi](https://github.com/wihlarkop/ipyapi)
- **Issue Tracker**: [github.com/wihlarkop/ipyapi/issues](https://github.com/wihlarkop/ipyapi/issues)