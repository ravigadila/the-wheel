from wsgiref.simple_server import make_server, demo_app

if __name__ == '__main__':
    server = make_server('', 5000, demo_app)
    server.serve_forever()
