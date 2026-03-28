# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-03-29

### Added
- `ReturnType` enum (`OBJECT`, `DICT`, `PYDANTIC`) replacing string literals for `return_type` parameter
- Optional Pydantic v2 support via `ipyapi[pydantic]` extra — `ReturnType.PYDANTIC` returns a `PydanticIPLocation` model
- `get_batch()` method on both sync and async clients for looking up multiple IPs at once (async uses `asyncio.gather` for concurrency)
- Automatic retry with exponential backoff on 429 rate limit responses (`max_retries`, `retry_backoff` constructor params)
- Client-side IP address validation via stdlib `ipaddress` — raises `InvalidIPAddressError` before making a network request
- `latlong` field on `IPLocation` and `PydanticIPLocation` (combined lat/long string from API)
- `_BaseIPyAPI` shared base class — sync and async clients now share endpoint building, validation, and error handling logic
- `@overload` typed signatures on `get_location` and `get_batch` for precise IDE type inference per `ReturnType`
- One-click release workflow (`.github/workflows/release.yml`) via `workflow_dispatch` with version input, matrix test gate, auto-tagging, GitHub release creation, and PyPI publish

### Changed
- `get_location()` and `get_batch()` `return_type` parameter now accepts `ReturnType` enum instead of strings
- `publish.yml` now requires all Python 3.10–3.13 matrix tests to pass before publishing; uses PyPI Trusted Publishing (OIDC) — no API token needed
- `test.yml` build step now uses `uv pip install --system` instead of `pip install --break-system-packages`
- Minimum Python version corrected to 3.10 (was incorrectly stated as 3.9 in docs)

### Fixed
- `_handle_error_response` except clause narrowed from `(ValueError, KeyError)` to `ValueError` — `.get()` never raises `KeyError`

## [0.1.0] - 2025-11-01

### Added
- Initial release of ipyapi
- Synchronous client (`IPyAPI`) and asynchronous client (`AsyncIPyAPI`) for ipapi.co
- Complete location data retrieval, single field queries, raw response formats (JSON, XML, CSV, YAML, JSONP)
- Comprehensive error handling: `RateLimitError`, `InvalidIPAddressError`, `ReservedIPAddressError`, HTTP errors (400, 403, 404, 405)
- Data models: `IPLocation`, `ErrorResponse`
- Context manager support for both clients
- Convenience methods: `get_ip`, `get_city`, `get_country`, `get_country_name`, `get_timezone`, `get_currency`, `get_asn`, `get_org`
- GitHub Actions CI/CD workflows

[Unreleased]: https://github.com/wihlarkop/ipyapi/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/wihlarkop/ipyapi/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/wihlarkop/ipyapi/releases/tag/v0.1.0
