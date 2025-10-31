"""Exception classes for ipyapi."""


class IPyAPIError(Exception):
    """Base exception for all ipyapi errors."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        """Initialize exception.

        Args:
            message: Error message
            status_code: HTTP status code if applicable
        """
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class BadRequestError(IPyAPIError):
    """Raised when API returns 400 Bad Request."""

    def __init__(self, message: str = "Bad Request") -> None:
        """Initialize BadRequestError."""
        super().__init__(message, status_code=400)


class ForbiddenError(IPyAPIError):
    """Raised when API returns 403 Forbidden (Authentication Failed)."""

    def __init__(self, message: str = "Authentication Failed") -> None:
        """Initialize ForbiddenError."""
        super().__init__(message, status_code=403)


class NotFoundError(IPyAPIError):
    """Raised when API returns 404 Not Found."""

    def __init__(self, message: str = "Resource Not Found") -> None:
        """Initialize NotFoundError."""
        super().__init__(message, status_code=404)


class MethodNotAllowedError(IPyAPIError):
    """Raised when API returns 405 Method Not Allowed."""

    def __init__(self, message: str = "Method Not Allowed") -> None:
        """Initialize MethodNotAllowedError."""
        super().__init__(message, status_code=405)


class RateLimitError(IPyAPIError):
    """Raised when API returns 429 Too Many Requests (Rate Limited)."""

    def __init__(self, message: str = "API rate limit exceeded") -> None:
        """Initialize RateLimitError."""
        super().__init__(message, status_code=429)


class InvalidIPAddressError(IPyAPIError):
    """Raised when an invalid IP address is provided."""

    def __init__(self, ip_address: str) -> None:
        """Initialize InvalidIPAddressError.

        Args:
            ip_address: The invalid IP address
        """
        super().__init__(f"Invalid IP address: {ip_address}")


class ReservedIPAddressError(IPyAPIError):
    """Raised when a reserved IP address is provided."""

    def __init__(self, ip_address: str) -> None:
        """Initialize ReservedIPAddressError.

        Args:
            ip_address: The reserved IP address
        """
        super().__init__(f"Reserved IP address: {ip_address}")
