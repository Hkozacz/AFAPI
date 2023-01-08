from logger import logger


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

