"""Tests for data models."""

from ipyapi.models import ErrorResponse, IPLocation


def test_iplocation_from_dict():
    """Test IPLocation.from_dict method."""
    data = {
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

    location = IPLocation.from_dict(data)

    assert location.ip == "8.8.8.8"
    assert location.network == "8.8.8.0/24"
    assert location.version == "IPv4"
    assert location.city == "Mountain View"
    assert location.region == "California"
    assert location.region_code == "CA"
    assert location.country == "US"
    assert location.country_name == "United States"
    assert location.country_code == "US"
    assert location.country_code_iso3 == "USA"
    assert location.country_capital == "Washington"
    assert location.country_tld == ".us"
    assert location.continent_code == "NA"
    assert location.in_eu is False
    assert location.postal == "94035"
    assert location.latitude == 37.386
    assert location.longitude == -122.0838
    assert location.timezone == "America/Los_Angeles"
    assert location.utc_offset == "-0800"
    assert location.country_calling_code == "+1"
    assert location.currency == "USD"
    assert location.currency_name == "Dollar"
    assert location.languages == "en-US,es-US,haw,fr"
    assert location.country_area == 9629091.0
    assert location.country_population == 327167434
    assert location.asn == "AS15169"
    assert location.org == "Google LLC"


def test_iplocation_from_dict_with_nulls():
    """Test IPLocation.from_dict with null values."""
    data = {
        "ip": "8.8.8.8",
        "network": "8.8.8.0/24",
        "version": "IPv4",
        "city": None,
        "region": None,
        "region_code": None,
        "country": "US",
        "country_name": "United States",
        "country_code": "US",
        "country_code_iso3": "USA",
        "country_capital": None,
        "country_tld": ".us",
        "continent_code": "NA",
        "in_eu": False,
        "postal": None,
        "latitude": 37.386,
        "longitude": -122.0838,
        "timezone": "America/Los_Angeles",
        "utc_offset": "-0800",
        "country_calling_code": "+1",
        "currency": "USD",
        "currency_name": "Dollar",
        "languages": "en-US",
        "country_area": None,
        "country_population": None,
        "asn": "AS15169",
        "org": "Google LLC",
    }

    location = IPLocation.from_dict(data)

    assert location.city is None
    assert location.region is None
    assert location.region_code is None
    assert location.country_capital is None
    assert location.postal is None
    assert location.country_area is None
    assert location.country_population is None


def test_iplocation_from_dict_with_hostname():
    """Test IPLocation.from_dict with optional hostname field."""
    data = {
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
        "languages": "en-US",
        "country_area": 9629091.0,
        "country_population": 327167434,
        "asn": "AS15169",
        "org": "Google LLC",
        "hostname": "dns.google",
    }

    location = IPLocation.from_dict(data)
    assert location.hostname == "dns.google"


def test_error_response_from_dict():
    """Test ErrorResponse.from_dict method."""
    data = {"error": True, "reason": "Invalid IP Address", "message": "IP address is invalid"}

    error = ErrorResponse.from_dict(data)

    assert error.error is True
    assert error.reason == "Invalid IP Address"
    assert error.message == "IP address is invalid"


def test_error_response_defaults():
    """Test ErrorResponse with missing fields."""
    data = {}

    error = ErrorResponse.from_dict(data)

    assert error.error is True
    assert error.reason == ""
    assert error.message == ""


def test_iplocation_latlong_present():
    """latlong field is parsed when present in API response."""
    data = {
        "ip": "8.8.8.8", "network": "8.8.8.0/24", "version": "IPv4",
        "city": "Mountain View", "region": "California", "region_code": "CA",
        "country": "US", "country_name": "United States", "country_code": "US",
        "country_code_iso3": "USA", "country_capital": "Washington",
        "country_tld": ".us", "continent_code": "NA", "in_eu": False,
        "postal": "94035", "latitude": 37.386, "longitude": -122.0838,
        "timezone": "America/Los_Angeles", "utc_offset": "-0800",
        "country_calling_code": "+1", "currency": "USD",
        "currency_name": "Dollar", "languages": "en-US",
        "country_area": 9629091.0, "country_population": 327167434,
        "asn": "AS15169", "org": "Google LLC",
        "latlong": "37.386,-122.0838",
    }
    location = IPLocation.from_dict(data)
    assert location.latlong == "37.386,-122.0838"


def test_iplocation_latlong_absent():
    """latlong defaults to None when not in API response."""
    data = {
        "ip": "8.8.8.8", "network": "8.8.8.0/24", "version": "IPv4",
        "city": "Mountain View", "region": "California", "region_code": "CA",
        "country": "US", "country_name": "United States", "country_code": "US",
        "country_code_iso3": "USA", "country_capital": "Washington",
        "country_tld": ".us", "continent_code": "NA", "in_eu": False,
        "postal": "94035", "latitude": 37.386, "longitude": -122.0838,
        "timezone": "America/Los_Angeles", "utc_offset": "-0800",
        "country_calling_code": "+1", "currency": "USD",
        "currency_name": "Dollar", "languages": "en-US",
        "country_area": 9629091.0, "country_population": 327167434,
        "asn": "AS15169", "org": "Google LLC",
    }
    location = IPLocation.from_dict(data)
    assert location.latlong is None
