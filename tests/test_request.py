from papi.request import *
from tests.test_utils import assert_equal
from papi.mime import MimeType

# parse_path() tests

def test_parse_path_happy():
    expected = ('foo','bar','baz')
    actual = parse_path('/foo/bar/baz')
    assert_equal(expected, actual)

def test_parse_path_no_leading_slash():
    expected = ('foo','bar','baz')
    actual = parse_path('foo/bar/baz')
    assert_equal(expected, actual)

def test_parse_path_trailing_slash():
    expected = ('foo','bar','baz')
    actual = parse_path('/foo/bar/baz/')
    assert_equal(expected, actual)

def test_parse_path_root():
    expected = ()
    actual = parse_path('/')
    assert_equal(expected, actual)

def test_parse_path_empty():
    expected = ()
    actual = parse_path('')
    assert_equal(expected, actual)

# get_headers() tests

def test_get_headers_happy():
    env = {
        'HTTP_ACCEPT': 'text/plain',
        'HTTP_HOST': 'example.org',
    }
    expected = {
        'Accept': 'text/plain',
        'Host': 'example.org',
    }
    actual = get_headers(env)
    assert_equal(expected, actual)

# parse_request() tests

def test_parse_request_happy():
    env = {
        'HTTP_ACCEPT': 'text/plain',
        'HTTP_HOST': 'example.org',
        'CONTENT_TYPE': 'text/plain',
        'PATH_INFO': '/foo',
        'REQUEST_METHOD': 'GET',
        'QUERY_STRING': 'quux=bar',
    }
    expected = {
        'path': ('foo',),
        'accept': [
                MimeType('text', 'plain', {}),
            ],
        'content_type': MimeType('text', 'plain', {}),
        'headers': {
            'Host': 'example.org',
            'Accept': 'text/plain',
        },
        'query': {
            'quux': 'bar'
        },
        'method': 'GET',
        'input': None,
    }
    actual = parse_request(env)
    assert_equal(
        sorted(expected.items()),
        sorted(actual.items())
    )
