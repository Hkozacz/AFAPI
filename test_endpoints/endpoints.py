from models.HTTP import Request


def hello_world(request: Request) -> str:
    return request.body + str(request.query_params)


