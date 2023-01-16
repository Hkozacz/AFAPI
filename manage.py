from dispatcher.dispatcher import Dispatcher
from test_endpoints.schema import schema

dispatcher = Dispatcher(schema=schema)


async def app(scope, receive, send):
    assert scope["type"] == "http"
    response = await dispatcher.dispatch(scope, receive)
    await send(
        {
            "type": "http.response.start",
            "status": response.status,
            "headers": response.headers,
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": response.body,
        }
    )
