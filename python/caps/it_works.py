from wsgiref.simple_server import make_server, demo_app


def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [b"Hello World !"]

if __name__ == '__main__':
    server = make_server('', 5000, simple_app)
    server.serve_forever()
