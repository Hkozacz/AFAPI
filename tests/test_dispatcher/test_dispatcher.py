import pytest

from exceptions.HTTPResponseExceptions import HTTP404, HTTP405
from models.HTTP import Response


def test_get_endpoint_func(dispatcher, test_endpoint):
    dispatcher.schema[""].update(
        {
            "hello": {
                "methods": {"get": test_endpoint, "post": test_endpoint},
            },
            "methods": {
                "get": test_endpoint,
                "post": {"methods": {"update": test_endpoint}},
            },
        }
    )

    assert dispatcher.get_endpoint_func("/hello", "post") == test_endpoint
    assert dispatcher.get_endpoint_func("/hello", "get") == test_endpoint
    assert dispatcher.get_endpoint_func("/hello/", "post") == test_endpoint
    assert dispatcher.get_endpoint_func("/hello/", "get") == test_endpoint
    assert dispatcher.get_endpoint_func("/", "get") == test_endpoint
    assert dispatcher.get_endpoint_func("/methods/post", "update") == test_endpoint
    with pytest.raises(HTTP405):
        dispatcher.get_endpoint_func("/methods/post", "post")
    with pytest.raises(HTTP404):
        dispatcher.get_endpoint_func("/world", "get")


def test_get_response(dispatcher, test_endpoint, test_request):
    assert dispatcher.get_response(test_endpoint, test_request) == Response(
        status=200,
        headers=[[b"content-type", b"text/json"]],
        body=b'{"hello": "world"}',
    )


def test_read_headers(dispatcher):
    headers = dispatcher.read_headers(
        [[b"content-type", b"text/json"], [b"Authorisation", b"Basic TOKEN"]]
    )
    assert headers == {"content-type": "text/json", "Authorisation": "Basic TOKEN"}


def test_read_query_params(dispatcher):
    pass
