from papi.hateoas import *
from tests.test_utils import assert_equal

# join_path() tests

def test_join_path():
    expected = '/hello/world'
    actual = join_path(('hello', 'world'))
    assert_equal(expected, actual)

# join_url() tests

# hateoas() tests

def test_hateoas_happy():
    src = {'foo': 'bar'}
    actual = hateoas(('hello', 'world'), src)
    expected = {
        'foo': 'bar',
        '_parent': {'href': '/hello'},
        '_self': {'href': '/hello/world'},
        '_next': {'href': '/hello/world?page=2'},
        '_top': {'href': '/hello/world'},
    }
    assert_equal(sorted(expected.items()), sorted(actual.items()))

def test_hateoas_none():
    src = None
    actual = hateoas(('hello', 'world'), src)
    expected = {
        '_parent': {'href': '/hello'},
        '_self': {'href': '/hello/world'},
        '_next': {'href': '/hello/world?page=2'},
        '_top': {'href': '/hello/world'},
    }
    assert_equal(sorted(expected.items()), sorted(actual.items()))

def test_hateoas_paging():
    src = None
    actual = hateoas(('hello', 'world'), src, page=10)
    expected = {
        '_parent': {'href': '/hello'},
        '_self': {'href': '/hello/world?page=10'},
        '_next': {'href': '/hello/world?page=11'},
        '_prev': {'href': '/hello/world?page=9'},
        '_top': {'href': '/hello/world'},
    }
    assert_equal(sorted(expected.items()), sorted(actual.items()))

def test_hateoas_offset():
    src = None
    actual = hateoas(('hello', 'world'), src, offset=30, count=10)
    expected = {
        '_parent': {'href': '/hello'},
        '_self': {'href': '/hello/world?count=10&offset=30'},
        '_next': {'href': '/hello/world?count=10&offset=40'},
        '_prev': {'href': '/hello/world?count=10&offset=20'},
        '_top': {'href': '/hello/world?count=10'},
    }
    assert_equal(sorted(expected.items()), sorted(actual.items()))

def test_hateoas_empty():
    src = ''
    actual = hateoas(('hello', 'world'), src)
    expected = {
        '_value': '',
        '_parent': {'href': '/hello'},
        '_self': {'href': '/hello/world'},
        '_next': {'href': '/hello/world?page=2'},
        '_top': {'href': '/hello/world'},
    }
    assert_equal(sorted(expected.items()), sorted(actual.items()))

def test_hateoas_wrong_type():
    src = True
    actual = hateoas(('hello', 'world'), src)
    expected = {
        '_value': True,
        '_parent': {'href': '/hello'},
        '_self': {'href': '/hello/world'},
        '_next': {'href': '/hello/world?page=2'},
        '_top': {'href': '/hello/world'},
    }
    assert_equal(sorted(expected.items()), sorted(actual.items()))

def test_hateoas_string():
    src = 'bar'
    actual = hateoas(('hello', 'world'), src)
    expected = {
        '_value': 'bar',
        '_parent': {'href': '/hello'},
        '_self': {'href': '/hello/world'},
        '_next': {'href': '/hello/world?page=2'},
        '_top': {'href': '/hello/world'},
    }
    assert_equal(sorted(expected.items()), sorted(actual.items()))

def test_hateoas_non_dict_collection():
    src = ['bar']
    actual = hateoas(('hello', 'world'), src)
    expected = {
        '_value': ['bar'],
        '_parent': {'href': '/hello'},
        '_self': {'href': '/hello/world'},
        '_next': {'href': '/hello/world?page=2'},
        '_top': {'href': '/hello/world'},
    }
    assert_equal(sorted(expected.items()), sorted(actual.items()))
