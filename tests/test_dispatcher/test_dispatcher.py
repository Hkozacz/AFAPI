from dataclasses import asdict
from unittest.mock import MagicMock

import pytest

from exceptions.HTTPResponseExceptions import HTTP404, HTTP405
from models.HTTP import Request, Response


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


@pytest.mark.parametrize(
    "query_string, expected",
    [
        (
            b"param1=value1&param2=value2",
            {"param1": "value1", "param2": "value2"},
        ),
        (
            b"",
            {},
        ),
        (
            b"param1=value1",
            {"param1": "value1"},
        ),
        (
            b"param1=",
            {"param1": ""},
        ),
        (b"param1=value1&param1=value2", {"param1": "value2"}),
    ],
)
def test_read_query_params(dispatcher, query_string, expected):
    assert dispatcher.read_query_params(query_string) == expected


@pytest.mark.anyio
@pytest.mark.parametrize(
    "request_data, body, expected_result",
    [
        (
            {
                "query_string": b"param1=value1&param2=value2",
                "method": "GET",
                "path": "/test",
                "scheme": "http",
                "headers": [[b"header1", b"value1"], [b"header2", b"value2"]],
            },
            "",
            Request(
                query_params={"param1": "value1", "param2": "value2"},
                method="get",
                path="/test",
                scheme="http",
                headers={"header1": "value1", "header2": "value2"},
                body="",
            ),
        ),
        (
            {
                "query_string": b"",
                "method": "POST",
                "path": "/test",
                "scheme": "https",
                "headers": [[b"header1", b"value1"], [b"header2", b"value2"]],
            },
            {"body_key": "body_value"},
            Request(
                query_params={},
                method="post",
                path="/test",
                scheme="https",
                headers={"header1": "value1", "header2": "value2"},
                body={"body_key": "body_value"},
            ),
        ),
        (
            {
                "query_string": b"param1=value1&param2=value2",
                "method": "PUT",
                "path": "/test",
                "scheme": "http",
                "headers": [[b"header1", b"value1"], [b"header2", b"value2"]],
            },
            "test_body",
            Request(
                query_params={"param1": "value1", "param2": "value2"},
                method="put",
                path="/test",
                scheme="http",
                headers={"header1": "value1", "header2": "value2"},
                body="test_body",
            ),
        ),
        (
            {
                "query_string": b"param1=value1&param2=value2",
                "method": "DELETE",
                "path": "/test",
                "scheme": "http",
                "headers": [[b"header1", b"value1"], [b"header2", b"value2"]],
            },
            "test_body",
            Request(
                query_params={"param1": "value1", "param2": "value2"},
                method="delete",
                path="/test",
                scheme="http",
                headers={"header1": "value1", "header2": "value2"},
                body="test_body",
            ),
        ),
    ],
)
async def test_build_request(dispatcher, request_data, body, expected_result):
    async def mock_body(*args, **kwargs):
        return body

    dispatcher.read_body = mock_body
    result = await dispatcher.build_request(request_data, MagicMock())
    assert result == expected_result


@pytest.mark.parametrize(
    "exception, expected_response",
    [
        (
            HTTP404,
            Response(
                status=404,
                headers=[[b"content-type", b"text/json"]],
                body=b"Page not found",
            ),
        ),
        (
            HTTP405,
            Response(
                status=405,
                headers=[[b"content-type", b"text/json"]],
                body=b"Method not allowed",
            ),
        ),
    ],
)
def test_handle_http_error(dispatcher, exception, expected_response):
    response = dispatcher.handle_http_error(exception)
    assert asdict(response) == asdict(expected_response)
