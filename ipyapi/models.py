"""Data models for ipyapi responses."""

from dataclasses import dataclass
from typing import Any


@dataclass
class IPLocation:
    """Complete IP location information from ipapi.co."""

    ip: str
    """IP address"""

    network: str
    """Network range"""

    version: str
    """IP version (IPv4 or IPv6)"""

    city: str | None
    """City name"""

    region: str | None
    """Region name"""

    region_code: str | None
    """Region code"""

    country: str
    """Country code (ISO 3166-1 alpha-2)"""

    country_name: str
    """Country name"""

    country_code: str
    """Country code (same as country)"""

    country_code_iso3: str
    """Country code (ISO 3166-1 alpha-3)"""

    country_capital: str | None
    """Capital city of the country"""

    country_tld: str
    """Country top-level domain"""

    continent_code: str
    """Continent code"""

    in_eu: bool
    """Whether the country is in the European Union"""

    postal: str | None
    """Postal/ZIP code"""

    latitude: float
    """Latitude coordinate"""

    longitude: float
    """Longitude coordinate"""

    timezone: str
    """Timezone identifier"""

    utc_offset: str
    """UTC offset"""

    country_calling_code: str
    """International calling code"""

    currency: str
    """Currency code"""

    currency_name: str
    """Currency name"""

    languages: str
    """Comma-separated list of language codes"""

    country_area: float | None
    """Country area in square kilometers"""

    country_population: int | None
    """Country population"""

    asn: str
    """Autonomous System Number"""

    org: str
    """Organization name"""

    hostname: str | None = None
    """Hostname (optional field, requires hostname add-on)"""

    latlong: str | None = None
    """Combined latitude and longitude as comma-separated string (e.g. '37.386,-122.0838')"""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "IPLocation":
        """Create IPLocation from API response dictionary.

        Args:
            data: API response dictionary

        Returns:
            IPLocation instance
        """
        return cls(
            ip=data.get("ip", ""),
            network=data.get("network", ""),
            version=data.get("version", ""),
            city=data.get("city"),
            region=data.get("region"),
            region_code=data.get("region_code"),
            country=data.get("country", ""),
            country_name=data.get("country_name", ""),
            country_code=data.get("country_code", ""),
            country_code_iso3=data.get("country_code_iso3", ""),
            country_capital=data.get("country_capital"),
            country_tld=data.get("country_tld", ""),
            continent_code=data.get("continent_code", ""),
            in_eu=data.get("in_eu", False),
            postal=data.get("postal"),
            latitude=data.get("latitude", 0.0),
            longitude=data.get("longitude", 0.0),
            timezone=data.get("timezone", ""),
            utc_offset=data.get("utc_offset", ""),
            country_calling_code=data.get("country_calling_code", ""),
            currency=data.get("currency", ""),
            currency_name=data.get("currency_name", ""),
            languages=data.get("languages", ""),
            country_area=data.get("country_area"),
            country_population=data.get("country_population"),
            asn=data.get("asn", ""),
            org=data.get("org", ""),
            hostname=data.get("hostname"),
            latlong=data.get("latlong"),
        )


@dataclass
class ErrorResponse:
    """Error response from ipapi.co API."""

    error: bool
    """Whether an error occurred"""

    reason: str
    """Error reason/type"""

    message: str
    """Human-readable error message"""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ErrorResponse":
        """Create ErrorResponse from API response dictionary.

        Args:
            data: API response dictionary

        Returns:
            ErrorResponse instance
        """
        return cls(
            error=data.get("error", True),
            reason=data.get("reason", ""),
            message=data.get("message", ""),
        )


try:
    from pydantic import BaseModel, ConfigDict

    class PydanticIPLocation(BaseModel):
        """Pydantic model for IP location data. Requires pydantic>=2.0."""

        model_config = ConfigDict(extra="ignore")

        ip: str
        network: str
        version: str
        city: str | None = None
        region: str | None = None
        region_code: str | None = None
        country: str
        country_name: str
        country_code: str
        country_code_iso3: str
        country_capital: str | None = None
        country_tld: str
        continent_code: str
        in_eu: bool
        postal: str | None = None
        latitude: float
        longitude: float
        timezone: str
        utc_offset: str
        country_calling_code: str
        currency: str
        currency_name: str
        languages: str
        country_area: float | None = None
        country_population: int | None = None
        asn: str
        org: str
        hostname: str | None = None
        latlong: str | None = None

    _PYDANTIC_AVAILABLE = True

except ImportError:
    _PYDANTIC_AVAILABLE = False
    PydanticIPLocation = None  # type: ignore[assignment,misc]
