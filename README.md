# IPyAPI

[![Tests](https://github.com/wihlarkop/ipyapi/actions/workflows/test.yml/badge.svg)](https://github.com/wihlarkop/ipyapi/actions/workflows/test.yml)
[![Code Quality](https://github.com/wihlarkop/ipyapi/actions/workflows/lint.yml/badge.svg)](https://github.com/wihlarkop/ipyapi/actions/workflows/lint.yml)
[![PyPI version](https://badge.fury.io/py/ipyapi.svg)](https://badge.fury.io/py/ipyapi)
[![Python versions](https://img.shields.io/pypi/pyversions/ipyapi.svg)](https://pypi.org/project/ipyapi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern Python client library for the [ipapi.co](https://ipapi.co) IP geolocation API. Built with `httpx`, full async support, automatic retries, and optional Pydantic v2 models.

## Features

- **Sync & Async** — both `IPyAPI` and `AsyncIPyAPI` clients
- **Typed returns** — `ReturnType.OBJECT` (dataclass), `ReturnType.DICT`, or `ReturnType.PYDANTIC`
- **Optional Pydantic v2** — install with `ipyapi[pydantic]` to get validated Pydantic models
- **Batch lookups** — `get_batch()` for multiple IPs (async uses `asyncio.gather`)
- **Auto retry** — exponential backoff on 429 rate limit responses
- **IP validation** — client-side check before any network request
- **Complete API coverage** — all fields, all response formats (JSON, XML, CSV, YAML, JSONP)
- **Full type hints** — `@overload` signatures for precise IDE inference
- **Python 3.10+**

## Installation

```bash
pip install ipyapi
# or
uv add ipyapi
```

With optional Pydantic support:

```bash
pip install 'ipyapi[pydantic]'
# or
uv add 'ipyapi[pydantic]'
```

## Quick Start

### Synchronous

```python
from ipyapi import IPyAPI

with IPyAPI() as client:
    location = client.get_location("8.8.8.8")
    print(f"{location.city}, {location.country_name}")
    # Mountain View, United States
```

### Asynchronous

```python
import asyncio
from ipyapi import AsyncIPyAPI

async def main():
    async with AsyncIPyAPI() as client:
        location = await client.get_location("8.8.8.8")
        print(f"{location.city}, {location.country_name}")

asyncio.run(main())
```

## Usage Examples

### Return Types

```python
from ipyapi import IPyAPI, ReturnType

with IPyAPI() as client:
    # Default — returns IPLocation dataclass
    location = client.get_location("8.8.8.8")
    print(location.country_name)

    # As dict
    data = client.get_location("8.8.8.8", return_type=ReturnType.DICT)
    print(data["country_name"])

    # As Pydantic model (requires ipyapi[pydantic])
    model = client.get_location("8.8.8.8", return_type=ReturnType.PYDANTIC)
    print(model.country_name)
```

### Batch Lookup

```python
with IPyAPI() as client:
    results = client.get_batch(["8.8.8.8", "1.1.1.1"])
    for r in results:
        print(f"{r.ip} — {r.org}")
```

Async batch runs concurrently via `asyncio.gather`:

```python
async with AsyncIPyAPI() as client:
    results = await client.get_batch(["8.8.8.8", "1.1.1.1"])
```

### Retry Configuration

```python
# Retry up to 5 times on 429, with 2s base backoff (sleeps 2, 4, 8, 16, 32s)
with IPyAPI(max_retries=5, retry_backoff=2.0) as client:
    location = client.get_location("8.8.8.8")
```

### Single Fields

```python
with IPyAPI() as client:
    print(client.get_ip())
    print(client.get_city("8.8.8.8"))
    print(client.get_country("8.8.8.8"))
    print(client.get_country_name("8.8.8.8"))
    print(client.get_timezone("8.8.8.8"))
    print(client.get_currency("8.8.8.8"))
    print(client.get_asn("8.8.8.8"))
    print(client.get_org("8.8.8.8"))

    # Any field by name
    postal = client.get_field("postal", "8.8.8.8")
```

### Raw Response Formats

```python
with IPyAPI() as client:
    json_data = client.get_location_raw("8.8.8.8", format="json")
    xml_data  = client.get_location_raw("8.8.8.8", format="xml")
    csv_data  = client.get_location_raw("8.8.8.8", format="csv")
    yaml_data = client.get_location_raw("8.8.8.8", format="yaml")
```

### Error Handling

```python
from ipyapi import IPyAPI
from ipyapi.exceptions import InvalidIPAddressError, RateLimitError, IPyAPIError

with IPyAPI() as client:
    try:
        location = client.get_location("not-an-ip")
    except InvalidIPAddressError:
        print("Invalid IP address")
    except RateLimitError:
        print("Rate limited — retries exhausted")
    except IPyAPIError as e:
        print(f"API error {e.status_code}: {e.message}")
```

## API Reference

### Client constructors

```python
IPyAPI(
    api_key=None,       # API key for paid plans
    base_url="https://ipapi.co",
    timeout=10.0,       # seconds
    max_retries=3,      # retries on 429
    retry_backoff=1.0,  # base backoff in seconds (sleeps backoff * 2^attempt)
)
```

`AsyncIPyAPI` accepts the same parameters.

### Methods

| Method | Returns |
|--------|---------|
| `get_location(ip=None, return_type=ReturnType.OBJECT)` | `IPLocation` / `dict` / `PydanticIPLocation` |
| `get_batch(ips, return_type=ReturnType.OBJECT)` | `list[IPLocation]` / `list[dict]` / `list[PydanticIPLocation]` |
| `get_field(field, ip=None)` | `str` |
| `get_location_raw(ip=None, format="json")` | `str` |
| `get_ip()` | `str` |
| `get_city(ip=None)` | `str` |
| `get_country(ip=None)` | `str` |
| `get_country_name(ip=None)` | `str` |
| `get_timezone(ip=None)` | `str` |
| `get_currency(ip=None)` | `str` |
| `get_asn(ip=None)` | `str` |
| `get_org(ip=None)` | `str` |

### IPLocation fields

`ip`, `network`, `version`, `city`, `region`, `region_code`, `country`, `country_name`, `country_code`, `country_code_iso3`, `country_capital`, `country_tld`, `continent_code`, `in_eu`, `postal`, `latitude`, `longitude`, `timezone`, `utc_offset`, `country_calling_code`, `currency`, `currency_name`, `languages`, `country_area`, `country_population`, `asn`, `org`, `hostname`, `latlong`

### Exceptions

All inherit from `IPyAPIError`:

| Exception | Trigger |
|-----------|---------|
| `InvalidIPAddressError` | Invalid IP format (raised client-side) |
| `ReservedIPAddressError` | Reserved/private IP (raised by API) |
| `BadRequestError` | 400 |
| `ForbiddenError` | 403 |
| `NotFoundError` | 404 |
| `MethodNotAllowedError` | 405 |
| `RateLimitError` | 429 after all retries exhausted |

## Development

```bash
git clone https://github.com/wihlarkop/ipyapi.git
cd ipyapi
uv sync --all-extras

uv run pytest                                    # run tests
uv run pytest --cov=ipyapi --cov-report=html     # with coverage
uv run ruff check ipyapi/ tests/                 # lint
uv run ruff format ipyapi/ tests/                # format
```

## Rate Limits

- **Free tier**: 1,000 requests/day, 30 requests/minute
- For higher limits see [ipapi.co pricing](https://ipapi.co/pricing/)

## License

MIT — see [LICENSE](LICENSE) for details.

## Links

- **API docs**: [ipapi.co/api](https://ipapi.co/api/)
- **PyPI**: [pypi.org/project/ipyapi](https://pypi.org/project/ipyapi/)
- **Source**: [github.com/wihlarkop/ipyapi](https://github.com/wihlarkop/ipyapi)
- **Issues**: [github.com/wihlarkop/ipyapi/issues](https://github.com/wihlarkop/ipyapi/issues)
