class HTTPResponseException(Exception):
    """Base Exception for HTTP responses"""

    message: str
    status_code: int


class HTTP404(HTTPResponseException):
    """Not found exception"""

    message = "Page not found"
    status_code = 404


class HTTP405(HTTPResponseException):
    """Method not allowed exception"""

    message = "Method not allowed"
    status_code = 405
