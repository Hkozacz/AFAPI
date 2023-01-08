from dispatcher.dispatcher import Dispatcher
from test_endpoints.schema import schema
from logger import logger

dispatcher = Dispatcher(schema=schema)


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    endpoint = dispatcher.get_endpoint_method(scope["path"], scope["method"])
    if type(endpoint) is int:
        status = endpoint
    else:
        response = endpoint(None, None)
        status = response["status"]
    await send({
        'type': 'http.response.start',
        'status': status,
        'headers': [
            [b'content-type', b'text/json'],
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello, world!',
    })