from papi.paths import *
from tests.test_utils import assert_equal
from collections import OrderedDict

# join_path() tests

def test_join_path():
    expected = '/hello/world'
    actual = join_path(('hello', 'world'))
    assert_equal(expected, actual)

# join_url() tests

def test_join_url_happy():
    expected = 'https://example.org/foo/bar?baz=quux&blah=pizza'
    actual = join_url(
        'https',
        'example.org',
        ['foo', 'bar'],
        OrderedDict([('baz','quux'), ('blah', 'pizza')]))

def test_join_url_no_proto():
    expected = '//example.org/foo/bar?baz=quux&blah=pizza'
    actual = join_url(
        domain='example.org',
        path=['foo', 'bar'],
        query=OrderedDict([('baz','quux'), ('blah', 'pizza')]))

def test_join_url_no_domain():
    expected = '/foo/bar?baz=quux&blah=pizza'
    actual = join_url(
        path=['foo', 'bar'],
        query=OrderedDict([('baz','quux'), ('blah', 'pizza')]))
