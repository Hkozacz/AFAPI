
# AFAPI 0.0.1 (Work in progress)

Sometimes, we just want to create some endpoint and don't think about anything else.
Sure FastAPI is easy, but i still felt that setting up some basic endpoints can be easier and quicker.
And that is main goal of AFAPI or easy as f... API.



## When should i use AFAPI?

* When you just want to quickly share a function with API endpoint.
* When your request data and response data isn't complicated.
* When you need to quickly show prof of concept.
* When you need efficienty in building more than performance.

## How to use it?
Very simple!
#### prepare endpoint function

```python
  def hello_world(request):
    return "Hello world"
```
Only required thing is that your endpoind function needs to take
only one argument, that will be your request data.

Then you have to declare your endpoint in `schema.py`

in 0.0.1 version, which is current version you need to pass your schema dict as
argument to initilize dispatcher in `main.py`
```python
from test_endpoints.schema import schema
dispatcher = Dispatcher(schema=schema)
```
ultimately it will be happening automatically, user will just have to create
`schema/schema.py`

### Setting up schema (routing)
We are trying to make setting up API schema (or routing) as easy
as possible. Setting this up with dict approach, make it clear
and easy to mantain. To create endpoint we need to add entry to schem dict:
```python
schema = {
    "": {
```
API schema always needs to start with root path "", every child to root path, needs to be
added to root dict so, if we want our path to hello_world function to look like
`www.example.com/hello/`: we need to create:
```python
schema = {
    "": {
        "hello": {
            "methods": {
                "get": hello_world
            }
        }
    }
}
```
or if we want it to look like `www.example.com/hello/world/`
```python
schema = {
    "": {
        "hello": {
          "world":{
            "methods": {
                "get": hello_world
              }
            }
        }
    }
}
```
Currently, every "path" need to have `methods` keyword at the end. ultimately we would want it to be optional.
Do not fear if you want your path to look like `www.example.com/hello/methods/get`
your schema should look like this then:

```python
schema = {
    "": {
        "hello": {
            "methods": {
                "get": {
                  "methods": {
                    "get": hello_world
                  }
                }
              }
            }
          }
        }
```

And Voila! we have our endpoint set! isn't that east AF?

# Request data
request thata have couple fo easy accessible parameters!

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `method` | `string` | Method of request (get, post, put...) in lower case |
| `path` | `string` | path of request |
| `scheme` | `string` | http or https |
| `query_params` | `dict` | url query params serialized as dict |
| `headers` | `dict` | headers serialized as dict |
| `body` | `dict or string` | serialized body of a reuqest. |

# Response data
You can `return` anything serializable (everything except objects, callables etc.)
dispatcher will automatically serialize it!

# TODO
* Make schema initializing automatic with using CLI
* create CLI for creating necessery files in project, and starting server
* make methods part of schema Optional (assume that all methods are allowed)
* publish package an pypi
