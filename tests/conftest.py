import pytest

from dispatcher.dispatcher import Dispatcher
from models.HTTP import Request


def hello_world(request):
    return {"hello": "world"}


@pytest.fixture
def dispatcher():
    return Dispatcher(schema={"": {}})


@pytest.fixture
def test_endpoint():
    return hello_world


@pytest.fixture
def test_request():
    return Request(
        query_params={"created_at": "12-12-2022", "statuses": ["shipped", "paid"]},
        method="get",
        path="hello/world",
        scheme="https",
        headers={"Authorisation": "Basic TOKEN"},
        body="Hello world",
    )
