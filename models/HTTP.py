from dataclasses import dataclass


@dataclass
class Response:
    status: int
    headers: list[list[bytes]]
    body: dict[bytes, bytes] | bytes


@dataclass
class Request:
    query_params: dict
    method: str
    path: str
    scheme: str
    headers: dict
    body: dict | str
