# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-11-01

### Added
- Initial release of ipyapi
- Complete synchronous client (`IPyAPI`) for ipapi.co API
- Complete asynchronous client (`AsyncIPyAPI`) for ipapi.co API
- Support for all API endpoints:
  - Complete location data retrieval
  - Single field queries
  - Multiple response formats (JSON, XML, CSV, YAML, JSONP)
- Comprehensive error handling:
  - `RateLimitError` for 429 responses
  - `InvalidIPAddressError` for invalid IP addresses
  - `ReservedIPAddressError` for reserved/private IPs
  - HTTP error exceptions (400, 403, 404, 405)
- Type hints throughout the codebase
- Data models (`IPLocation`, `ErrorResponse`)
- Context manager support for both sync and async clients
- Convenience methods for common fields (get_ip, get_country, etc.)
- Comprehensive test suite with 94% coverage
- Full documentation with examples
- GitHub Actions CI/CD workflows
- Support for Python 3.9+

### Changed
- N/A (initial release)

### Deprecated
- N/A (initial release)

### Removed
- N/A (initial release)

### Fixed
- N/A (initial release)

### Security
- N/A (initial release)

---

## Version History

### Versioning Strategy

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backward compatible manner
- **PATCH** version for backward compatible bug fixes

### Release Stages

- **0.x.x** - Alpha/Beta releases, API may change
- **1.0.0+** - Stable releases, following strict SemVer

### Future Roadmap

Planned for future versions:
- **0.2.0** - Add retry mechanism with exponential backoff
- **0.3.0** - Add caching support
- **1.0.0** - First stable release after real-world testing

[Unreleased]: https://github.com/wihlarkop/ipyapi/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/wihlarkop/ipyapi/releases/tag/v0.1.0
