"""Tests for _BaseIPyAPI shared base class."""

from unittest.mock import MagicMock

import pytest

from ipyapi._base_client import _BaseIPyAPI
from ipyapi.exceptions import (
    BadRequestError,
    ForbiddenError,
    InvalidIPAddressError,
    MethodNotAllowedError,
    NotFoundError,
    RateLimitError,
    ReservedIPAddressError,
)


@pytest.fixture
def base():
    return _BaseIPyAPI()


def test_base_default_init(base):
    assert base._base_url == "https://ipapi.co"
    assert base._api_key is None
    assert base._max_retries == 3
    assert base._retry_backoff == 1.0


def test_base_custom_init():
    b = _BaseIPyAPI(
        api_key="key123",
        base_url="https://custom.co/",
        timeout=5.0,
        max_retries=5,
        retry_backoff=2.0,
    )
    assert b._base_url == "https://custom.co"  # trailing slash stripped
    assert b._api_key == "key123"
    assert b._max_retries == 5
    assert b._retry_backoff == 2.0
    assert b._timeout == 5.0


def test_build_endpoint_with_ip(base):
    assert base._build_endpoint("8.8.8.8", "json") == "8.8.8.8/json/"


def test_build_endpoint_without_ip(base):
    assert base._build_endpoint(None, "json") == "json/"


def test_build_endpoint_field_with_ip(base):
    assert base._build_endpoint("1.1.1.1", "country") == "1.1.1.1/country/"


def test_build_endpoint_field_without_ip(base):
    assert base._build_endpoint(None, "country") == "country/"


def test_validate_ip_valid_ipv4(base):
    base._validate_ip("8.8.8.8")  # should not raise


def test_validate_ip_valid_ipv6(base):
    base._validate_ip("2001:4860:4860::8888")  # should not raise


def test_validate_ip_invalid(base):
    with pytest.raises(InvalidIPAddressError):
        base._validate_ip("not-an-ip")


def test_validate_ip_invalid_partial(base):
    with pytest.raises(InvalidIPAddressError):
        base._validate_ip("999.999.999.999")


def test_handle_error_400_invalid_ip(base):
    response = MagicMock()
    response.status_code = 400
    response.json.return_value = {"error": True, "reason": "Invalid IP Address", "message": "bad"}
    with pytest.raises(InvalidIPAddressError):
        base._handle_error_response(response)


def test_handle_error_400_reserved_ip(base):
    response = MagicMock()
    response.status_code = 400
    response.json.return_value = {"error": True, "reason": "Reserved IP Address", "message": "rsv"}
    with pytest.raises(ReservedIPAddressError):
        base._handle_error_response(response)


def test_handle_error_400_generic(base):
    response = MagicMock()
    response.status_code = 400
    response.json.return_value = {"error": True, "reason": "Other", "message": "bad"}
    with pytest.raises(BadRequestError):
        base._handle_error_response(response)


def test_handle_error_400_malformed_json(base):
    response = MagicMock()
    response.status_code = 400
    response.json.side_effect = ValueError("not json")
    with pytest.raises(BadRequestError, match="Bad Request"):
        base._handle_error_response(response)


def test_handle_error_403(base):
    response = MagicMock()
    response.status_code = 403
    with pytest.raises(ForbiddenError):
        base._handle_error_response(response)


def test_handle_error_404(base):
    response = MagicMock()
    response.status_code = 404
    with pytest.raises(NotFoundError):
        base._handle_error_response(response)


def test_handle_error_405(base):
    response = MagicMock()
    response.status_code = 405
    with pytest.raises(MethodNotAllowedError):
        base._handle_error_response(response)


def test_handle_error_429(base):
    response = MagicMock()
    response.status_code = 429
    with pytest.raises(RateLimitError):
        base._handle_error_response(response)
