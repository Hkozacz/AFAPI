from test_endpoints.endpoints import hello_world

schema = {
    "": {
        "hello": {
            "methods": {
                "get": hello_world
            }
        }
    }
}