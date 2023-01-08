from models.HTTP import Response


def hello_world(request, header) -> dict:
    return {"hello": "world"}