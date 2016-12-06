from papi.serve import serve_resource
import papi.fp as fp
from papi.mime import match_mime, parse_mime_type
from papi.exceptions import ResourceException
from tests.test_utils import assert_equal, assert_equal_dicts
import json

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

def parse_json_body(response):
    response['body'] = json.loads(response['body'].decode('utf-8'))
    return response

def test_root_get_json():
    class MyResource(object):
        def get_typed_body(self, *args, **kwargs):
            return None

        def get_structured_body(self, *args, **kwargs):
            return {"bird":"canary"}

    def application(env, start_response):
        return serve_resource(MyResource())(env, start_response)

    expected = {
        'status': '200 OK',
        'headers': [('Content-type', 'text/json')],
        'body': {"bird": "canary"}
    }
    actual = parse_json_body(
        mock_request(application, "GET", "/",
            query='hateoas=off',
            headers=[("Accept", "text/json")]))
    assert_equal_dicts(expected, actual)

def test_root_get_json_with_hateoas():
    class MyResource(object):
        def get_typed_body(self, *args, **kwargs):
            return None

        def get_structured_body(self, *args, **kwargs):
            return {"bird":"canary"}

    def application(env, start_response):
        return serve_resource(MyResource())(env, start_response)

    expected = {
        'status': '200 OK',
        'headers': [('Content-type', 'text/json')],
        'body': {
            "bird": "canary",
            "_parent": { "href": "/" },
            "_self": { "href": "/?page=1" },
            "_next": { "href": "/?page=2"},
            "_top": { "href": "/"}
        }
    }
    actual = parse_json_body(
        mock_request(application, "GET", "/",
            query='hateoas=on',
            headers=[("Accept", "text/json")]))
    assert_equal_dicts(expected, actual)

def test_child_get():
    class MyChildResource(object):
        def get_typed_body(self, *args, **kwargs):
            return parse_mime_type("text/plain"), "HI!"

    class MyRootResource(object):
        def get_typed_body(self, *args, **kwargs):
            return {}
        def get_child(self, name, *args, **kwargs):
            assert_equal(name, "hello")
            return MyChildResource()

    def application(env, start_response):
        return serve_resource(MyRootResource())(env, start_response)

    expected = {
        'status': '200 OK',
        'headers': [('Content-type', 'text/plain')],
        'body': b'HI!'
    }
    actual = mock_request(application, "GET", "/hello")
    assert_equal(expected, actual)
