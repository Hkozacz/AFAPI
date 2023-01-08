import logging
logger = logging.getLogger("uvicorn")

async def app(scope, receive, send):
    assert scope['type'] == 'http'
    x = await receive()
    logger.info(scope["path"])
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/plain'],
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello, world!',
    })