from dataclasses import dataclass


@dataclass
class Response:
    """Response model, containing data to send in response to client."""

    status: int
    headers: list[list[bytes]]
    body: dict[bytes, bytes] | bytes


@dataclass
class Request:
    """Request model, containing request data."""

    query_params: dict
    method: str
    path: str
    scheme: str
    headers: dict
    body: dict | str
