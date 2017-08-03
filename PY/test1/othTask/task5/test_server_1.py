from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher


@dispatcher.add_method
def foobar(**kwargs):
    return kwargs["foo"] + kwargs["bar"] + kwargs["hew"]

@dispatcher.add_method
def test_add(*args):
    s=0
    for v in args:
        if type(v)!=type(1):
            return 'wrong value'
        s +=v
    return s


@Request.application
def application(request):
    # Dispatcher is dictionary {<method_name>: callable}
    dispatcher["echo"] = lambda s: s
    dispatcher["add"] = lambda a, b: a + b

    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('localhost', 4000, application)