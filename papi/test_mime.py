from papi.mime import *
from papi.test_utils import assert_equal

def test_parse_mime_simple():
    src = "text/plain"
    expected = ("text", "plain", {})
    actual = parse_mime_type(src)
    assert_equal(expected, actual)

def test_parse_mime_wildcard():
    src = "text/*"
    expected = ("text", "*", {})
    actual = parse_mime_type(src)
    assert_equal(expected, actual)

def test_parse_mime_props():
    src = "text/plain;charset=utf8;q=0.2"
    expected = ("text", "plain", {"charset":"utf8", "q": "0.2"})
    actual = parse_mime_type(src)
    assert_equal(expected, actual)

def test_parse_mime_degenerate():
    src = "text/plain;charset;q=0.2"
    expected = ("text", "plain", {"charset":"", "q": "0.2"})
    actual = parse_mime_type(src)
    assert_equal(expected, actual)

def test_parse_http_accept():
    src = "text/plain;q=0.6,text/*;q=0.3,*/*;q=0.1"
    expected = [
        ("text", "plain", {"q": "0.6"}),
        ("text", "*", {"q":"0.3"}),
        ("*", "*", {"q":"0.1"})
    ]
    actual = parse_http_accept(src)
    assert_equal(expected, actual)

def test_parse_http_accept():
    src = "text/*;q=0.3,text/plain;q=0.6,*/*;q=0.1"
    expected = [
        ("text", "plain", {"q": "0.6"}),
        ("text", "*", {"q":"0.3"}),
        ("*", "*", {"q":"0.1"})
    ]
    actual = parse_http_accept(src, sort=True)
    assert_equal(expected, actual)

def test_parse_http_accept_spaces():
    src = "text/plain; q=0.6 ,text/* ; q =0.3, */* ;q=0.1"
    expected = [
        ("text", "plain", {"q": "0.6"}),
        ("text", "*", {"q":"0.3"}),
        ("*", "*", {"q":"0.1"})
    ]
    actual = parse_http_accept(src)
    assert_equal(expected, actual)

def test_match_mime_positives():
    pairs = [
        ("*/*", "text/plain", ()),
        ("*/*", "application/json", ()),
        ("text/*", "text/html", ()),
        ("text/plain", "text/plain", ()),
        ("text/plain;charset=utf8", "text/plain;charset=utf8", ("charset",)),
        ("text/plain;charset=utf8", "text/plain;charset=utf8", ("charset", "q")),
        ("text/plain", "text/plain;charset=utf8", ("charset", "q")),
    ]
    for pattern_str, candidate_str, props in pairs:
        pattern = parse_mime_type(pattern_str)
        candidate = parse_mime_type(candidate_str)
        assert(match_mime(pattern, candidate, props))

def test_match_mime_negatives():
    pairs = [
        ("text/*", "application/json", ()),
        ("text/plain;charset=latin1", "text/plain;charset=utf8", ("charset",)),
        ("text/plain;charset=utf8", "text/plain", ("charset", "q")),
    ]
    for pattern_str, candidate_str, props in pairs:
        pattern = parse_mime_type(pattern_str)
        candidate = parse_mime_type(candidate_str)
        assert(not match_mime(pattern, candidate, props))
