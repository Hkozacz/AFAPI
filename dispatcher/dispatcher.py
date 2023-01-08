import json

from exceptions.HTTPResponseExceptions import HTTP404, HTTP405, HTTPResponseException
from models.HTTP import Request, Response


class Dispatcher:
    """
    Dispatcher service for dispatching events to proper endpoints
    and serializing them.
    """

    def __init__(self, schema: dict[str, callable]):
        self.schema = schema

    def get_endpoint_func(self, path: str, method: str) -> callable:
        """
        Get endpoint function based on path.
        :param path: path of request
        :param method: method of request
        :return: callable function matched with path
        """
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
        """
        Serialize func return as Response model

        :param func: callable function matched with path
        :param request: Request object model
        :return: returns serialized Response model object
        """
        response_body = func(request)
        return Response(
            status=200,
            headers=[[b"content-type", b"text/json"]],
            body=json.dumps(response_body).encode("utf-8"),
        )

    @staticmethod
    async def read_body(receive: callable) -> dict | str:
        """
        Read and return the entire body from an incoming ASGI message
        and serialize it as a dict.

        :param receive: callable cuarantine containing body message of request
        :return: returns serialized request body as a string or json
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
        """
        Serialize headers as a dict

        :param headers: list of headers as bytes
        :return: serialized headers in dict form
        """
        return {key.decode("utf-8"): value.decode("utf-8") for key, value in headers}

    @staticmethod
    def read_query_params(query_string: bytes) -> dict:
        """
        Serialize query params as a dict

        :param query_string: query params as string.
        :return: query params as dict.
        """
        query_list = query_string.decode("utf-8").split("&")
        return {
            param[: param.find("=")]: param[param.find("=") + 1 :]
            for param in query_list
        }

    async def build_request(self, request_data: dict, receive: callable) -> Request:
        """
        Serialize request data as Request model object.

        :param request_data: dict with request data such as method, path etc.
        :param receive: callable quarantine containing request body in bytes
        :return: Request model object
        """
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
        """
        Serizalize exception as Response model object with proper status code and body
        :param exception: HTTP Exception like HTTP404 exception.
        :return: Response model object.
        """
        return Response(
            status=exception.status_code,
            headers=[[b"content-type", b"text/json"]],
            body=exception.message.encode("utf-8"),
        )

    async def dispatch(self, request_data: dict, receive: callable) -> Response:
        """
        Method for using reuqest data with proper endpoint function.
        :param request_data: dict with request data such as method, path etc.
        :param receive: callable quarantine containing request body in bytes
        :return: Response model object
        """
        request = await self.build_request(request_data, receive)
        try:
            func = self.get_endpoint_func(request.path, request.method)
        except HTTPResponseException as http_error:
            return self.handle_http_error(http_error)
        return self.get_response(func, request)
