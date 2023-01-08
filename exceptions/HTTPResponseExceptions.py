class HTTPResponseException(Exception):
    message: str
    status_code: int


class HTTP404(HTTPResponseException):
    message = "Page not found"
    status_code = 404


class HTTP405(HTTPResponseException):
    message = "Method not allowed"
    status_code = 405

