import urllib.parse
import http.client
import re
from wsgiref.simple_server import make_server
from wsgiref.headers import Headers



class NotFound(Exception):
    pass


class Request:
	def __init__(self, environ):
		self.environ = environ
	@property
	def args(self):
		get_args = urllib.parse.parse_qs(self.environ['QUERY_STRING'])
		return { k: v[0] for k, v in get_args.items()}

	@property
	def path(self):
		return self.environ['PATH_INFO']

class Response:

	def __init__(self, response=None, status=200, charset='utf-8', content_type='text/html'):
		self.response = [] if response is None else response
		self.charset = charset
		self.headers = Headers()
		self.headers.add_header('content-type', '{content_type}; charset={charset})'.format(content_type=content_type, charset=charset))
		self._status = status

	@property
	def status(self):
		status_string = http.client.responses.get(self._status, "UNKNOWN")
		return '{status} {status_string}'.format(status=self._status, status_string=status_string)

	def __iter__(self):
		for k in self.response:
			if isinstance(k, bytes):
				yield k
			else:
				yield k.encode(self.charset)

def request_response_application(function):
	def application(environ, start_response):
		request = Request(environ)
		response = function(request)
		start_response(response.status, response.headers.items())
		return iter(response)
	return application



def hello(request, name):
	return Response([
		'<doctype html>'
		'<html>',
		'<body><h1>Hello {name} !'.format(name=name),
		'</html>'
		])

def goodbye(request, name):
	return Response([
		'<doctype html>'
		'<html>',
		'<body><h1>GoodBye {name} !'.format(name=name),
		'</html>'
		])

class Router:

	def __init__(self):
		self.route_table = []

	def add_route(self, pattern, callback):
		self.route_table.append((pattern, callback))

	def match(self, path):
		for (pattern, callback) in self.route_table:
			m = re.match(pattern, path)
			if m:
				return (callback, m.groups())
		raise NotFound()


routes = Router()
routes.add_route(r'/hello/(.*)/$', hello)
routes.add_route(r'/goodbye/(.*)/$', goodbye)



def application(environ, start_response):
	try:
		request = Request(environ)
		callback, args = routes.match(request.path)
		response = callback(request, *args)
	except NotFound:
		response = Response(b'<h1>NotFound</h1>', status=404)

	start_response(response.status, response.headers.items())
	return iter(response)

if __name__ == '__main__':
	server = make_server('', 5000, application)
	server.serve_forever()
