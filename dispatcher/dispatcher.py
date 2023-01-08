import json

from exceptions.HTTPResponseExceptions import HTTP404, HTTP405, HTTPResponseException
from models.HTTP import Request, Response


class Dispatcher:
    def __init__(self, schema: dict[str, callable]):
        self.schema = schema

    def get_endpoint_method(self, path: str, method: str):
        path_items = path.split("/")
        curr = self.schema
        for item in path_items:
            try:
                curr = curr[item]
            except KeyError:
                raise HTTP404
        try:
            return curr["methods"][method]
        except KeyError:
            raise HTTP405

    @staticmethod
    def get_response(func: callable, request: Request) -> Response:
        response_body = func(request)
        return Response(
            status=200,
            headers=[[b"content-type", b"text/json"]],
            body=json.dumps(response_body).encode("utf-8"),
        )

    @staticmethod
    async def read_body(receive: callable) -> dict | str:
        """
        Read and return the entire body from an incoming ASGI message.
        """
        body = b""
        more_body = True

        while more_body:
            message = await receive()
            body += message.get("body", b"")
            more_body = message.get("more_body", False)
        decoded_body = body.decode("utf-8")
        try:
            decoded_body = json.loads(decoded_body)
        except json.decoder.JSONDecodeError:
            pass
        return decoded_body

    @staticmethod
    def read_headers(headers: list) -> dict:
        return {key.decode("utf-8"): value.decode("utf-8") for key, value in headers}

    @staticmethod
    def read_query_params(query_string: bytes) -> dict:
        query_list = query_string.decode("utf-8").split("&")
        return {
            param[: param.find("=")]: param[param.find("=") + 1 :]
            for param in query_list
        }

    async def build_request(self, request_data: dict, receive: callable) -> Request:
        return Request(
            query_params=self.read_query_params(request_data["query_string"]),
            method=request_data["method"].lower(),
            path=request_data["path"],
            scheme=request_data["scheme"],
            headers=self.read_headers(request_data["headers"]),
            body=await self.read_body(receive),
        )

    @staticmethod
    def handle_http_error(exception: HTTPResponseException) -> Response:
        return Response(
            status=exception.status_code,
            headers=[[b"content-type", b"text/json"]],
            body=exception.message.encode("utf-8"),
        )

    async def dispatch(self, request_data: dict, receive: callable) -> Response:
        request = await self.build_request(request_data, receive)
        try:
            func = self.get_endpoint_method(request.path, request.method)
        except HTTPResponseException as http_error:
            return self.handle_http_error(http_error)
        return self.get_response(func, request)
