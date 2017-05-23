HELLO_WORLD = b"Hello Ravi!\n"

def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    name = str.encode(environ['QUERY_STRING'])  # parse this string.
    Output = b"Hello " + name
    return [Output]


from wsgiref.simple_server import make_server, demo_app

if __name__ == '__main__':
    server = make_server('', 5000, simple_app)
    server.serve_forever()
