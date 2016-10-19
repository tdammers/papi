from papi.hateoas import *
from tests.test_utils import assert_equal

# join_path() tests

def test_join_path():
    expected = '/hello/world'
    actual = join_path(('hello', 'world'))
    assert_equal(expected, actual)

# hateoas() tests

def test_hateoas_happy():
    src = {'foo': 'bar'}
    actual = hateoas(('hello', 'world'), src)
    expected = {
        'foo': 'bar',
        '_parent': {'href': '/hello'},
        '_self': {'href': '/hello/world'},
    }
    assert_equal(expected, actual)

def test_hateoas_none():
    src = ''
    actual = hateoas(('hello', 'world'), src)
    expected = {
        '_value': '',
        '_parent': {'href': '/hello'},
        '_self': {'href': '/hello/world'},
    }
    assert_equal(expected, actual)

def test_hateoas_empty():
    src = ''
    actual = hateoas(('hello', 'world'), src)
    expected = {
        '_value': '',
        '_parent': {'href': '/hello'},
        '_self': {'href': '/hello/world'},
    }
    assert_equal(expected, actual)

def test_hateoas_wrong_type():
    src = True
    actual = hateoas(('hello', 'world'), src)
    expected = {
        '_value': True,
        '_parent': {'href': '/hello'},
        '_self': {'href': '/hello/world'},
    }
    assert_equal(expected, actual)

def test_hateoas_string():
    src = 'bar'
    actual = hateoas(('hello', 'world'), src)
    expected = {
        '_value': 'bar',
        '_parent': {'href': '/hello'},
        '_self': {'href': '/hello/world'},
    }
    assert_equal(expected, actual)

def test_hateoas_non_dict_collection():
    src = ['bar']
    actual = hateoas(('hello', 'world'), src)
    expected = {
        '_value': ['bar'],
        '_parent': {'href': '/hello'},
        '_self': {'href': '/hello/world'},
    }
    assert_equal(expected, actual)
