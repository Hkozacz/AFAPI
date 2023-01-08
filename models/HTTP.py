from dataclasses import dataclass


@dataclass
class Response:
    status: int
    headers: dict
    body: dict[bytes, bytes] | str
