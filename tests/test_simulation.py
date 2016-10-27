from papi.serve import serve_resource
import papi.fp as fp
from papi.mime import match_mime, parse_mime_type
from papi.exceptions import ResourceException
from tests.test_utils import assert_equal

def mock_request(
        application,
        method,
        path,
        query="",
        headers=(),
        request_body=""):
    env = {}
    env['PATH_INFO'] = path
    env['QUERY_STRING'] = query
    env['REQUEST_METHOD'] = method
    env['CONTENT_TYPE'] = "text/plain"
    env['wsgi.input'] = None
    for name, value in headers:
        massaged_name = "_".join(fp.cons("HTTP", name.split("-"))).upper()
        env[massaged_name] = value
        if name.casefold() == "Content-Type".casefold():
            env['CONTENT_TYPE'] = value
    response = {}
    def start_response(status_str, headers):
        response['status'] = status_str
        response['headers'] = headers

    response['body'] = application(env, start_response)
    return response

def test_root_get():
    class MyResource(object):
        def get_typed_body(self, *args, **kwargs):
            return parse_mime_type("text/plain"), "HI!"

    def application(env, start_response):
        return serve_resource(MyResource())(env, start_response)

    expected = {
        'status': '200 OK',
        'headers': [('Content-type', 'text/plain')],
        'body': b'HI!'
    }
    actual = mock_request(application, "GET", "/")
    assert_equal(expected, actual)
