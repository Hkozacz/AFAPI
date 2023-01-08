from logger import logger
from models.HTTP import Response


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
                return 404
        try:
            method = method.lower()
            return curr["methods"][method]
        except KeyError:
            return 405

    @staticmethod
    def get_response(func: callable) -> Response:
        response_body = func(None, None)


