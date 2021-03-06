from papi.fp import *
from papi.fp import _tuplize
from tests.test_utils import assert_equal

# tests for internal helpers

def test__tuplize_happy():
    expected = (1,2,3)
    actual = _tuplize([1,2,3])
    assert_equal(expected, actual)

def test__tuplize_none():
    expected = ()
    actual = _tuplize(None)
    assert_equal(expected, actual)

def test__tuplize_string():
    expected = ("hello",)
    actual = _tuplize("hello")
    assert_equal(expected, actual)

def test__tuplize_scalar():
    expected = (1,)
    actual = _tuplize(1)
    assert_equal(expected, actual)

# fmap() tests

def test_fmap_list():
    expected = (2,3,4)
    actual = tuple(fmap(lambda x: x + 1, (1,2,3)))
    assert_equal(expected, actual)

def test_fmap_dict():
    expected = {"foo": 2, "bar": 3}
    actual = fmap(lambda x: x + 1, {"foo": 1, "bar": 2})
    assert_equal(expected, actual)

def test_fmap_fn():
    def foo():
        return 1
    expected = 2
    actual = (fmap(lambda x: x + 1, foo))()
    assert_equal(expected, actual)

def test_fmap_fn_return_none():
    def foo():
        return None
    expected = None
    actual = (fmap(lambda x: x + 1, foo))()
    assert_equal(expected, actual)

def test_fmap_none():
    expected = None
    actual = fmap(lambda x: x + 1, None)
    assert_equal(expected, actual)

def test_fmap_scalar():
    expected = 2
    actual = fmap(lambda x: x + 1, 1)
    assert_equal(expected, actual)

# dictmap() tests

def test_dictmap_dict():
    expected = {"foo": 2, "bar": 3}
    actual = dictmap(lambda x: x + 1, {"foo": 1, "bar": 2})
    assert_equal(expected, actual)

# compose() tests

def test_compose():
    def a(i):
        return i * 7

    def b(i):
        return i + 5

    composed = compose(a, b)
    expected = (3 + 5) * 7
    actual = composed(3)
    assert_equal(expected, actual)

# chain() tests

def test_chain():
    def a(i):
        return i * 7

    def b(i):
        return i + 5

    composed = chain(a, b)
    expected = (3 + 5) * 7
    actual = composed(3)
    assert_equal(expected, actual)

def test_chain_empty():
    composed = chain()
    expected = 3
    actual = composed(3)
    assert_equal(expected, actual)

# rcompose() tests

def test_rcompose():
    def a(i):
        return i * 7

    def b(i):
        return i + 5

    composed = rcompose(a, b)
    expected = (3 * 7) + 5
    actual = composed(3)
    assert_equal(expected, actual)

# identity() tests

def test_identity():
    for i in [1, 23, None, (1,2,3), "hello"]:
        assert_equal(i, identity(i))

# assoc() tests

def test_assoc_normal():
    expected = {'foo': 'bar', 'baz': 'quux'}
    actual = assoc('baz', 'quux', {'foo':'bar'})
    assert_equal(expected, actual)

def test_assoc_empty():
    expected = {'baz': 'quux'}
    actual = assoc('baz', 'quux', {})
    assert_equal(expected, actual)

def test_assoc_on_none():
    expected = {'baz': 'quux'}
    actual = assoc('baz', 'quux', None)
    assert_equal(expected, actual)

def test_assoc_on_implicit():
    expected = {'baz': 'quux'}
    actual = assoc('baz', 'quux', None)
    assert_equal(expected, actual)

def test_assoc_overwrite():
    expected = {'baz': 'quux'}
    actual = assoc('baz', 'quux', {'baz':'bar'})
    assert_equal(expected, actual)

def test_assoc_immutable():
    expected = {'baz': 'bar'}
    a = {'baz':'bar'}
    assoc('baz', 'quux', a)
    actual = a
    assert_equal(expected, actual)

# dissoc() tests

def test_dissoc_normal():
    expected = {'foo':'bar'}
    actual = dissoc('baz', {'foo': 'bar', 'baz': 'quux'})
    assert_equal(expected, actual)

def test_dissoc_nonexistent():
    expected = {'foo':'bar'}
    actual = dissoc('baz', {'foo': 'bar' })
    assert_equal(expected, actual)

# assocs() tests

def test_assocs_normal():
    expected = {'foo': 'bar', 'baz': 'quux', 'pizza': 'olives'}
    actual = assocs([('foo', 'bar'), ('pizza', 'olives')], {'baz': 'quux'})
    assert_equal(expected, actual)

def test_assocs_empty():
    expected = {'foo': 'bar', 'pizza': 'olives'}
    actual = assocs([('foo', 'bar'), ('pizza', 'olives')], {})
    assert_equal(expected, actual)

def test_assocs_on_none():
    expected = {'foo': 'bar', 'pizza': 'olives'}
    actual = assocs([('foo', 'bar'), ('pizza', 'olives')], None)
    assert_equal(expected, actual)

def test_assocs_on_implicit():
    expected = {'foo': 'bar', 'pizza': 'olives'}
    actual = assocs([('foo', 'bar'), ('pizza', 'olives')], None)
    assert_equal(expected, actual)

# cons() tests

def test_cons_happy():
    expected = (1,2,3)
    actual = cons(1, (2,3))
    assert_equal(expected, actual)

def test_cons_list():
    expected = (1,2,3)
    actual = cons(1, [2,3])
    assert_equal(expected, actual)

def test_cons_immutable():
    expected = [2,3]
    a = [2,3]
    cons(1, a)
    actual = a
    assert_equal(expected, actual)

def test_cons_empy():
    expected = (1,)
    actual = cons(1, [])
    assert_equal(expected, actual)

def test_cons_none():
    expected = (1,)
    actual = cons(1, None)
    assert_equal(expected, actual)

# snoc() tests

def test_snoc_happy():
    expected = (2,3,1)
    actual = snoc(1, (2,3))
    assert_equal(expected, actual)

def test_snoc_list():
    expected = (2,3,1)
    actual = snoc(1, [2,3])
    assert_equal(expected, actual)

def test_snoc_immutable():
    expected = [2,3]
    a = [2,3]
    snoc(1, a)
    actual = a
    assert_equal(expected, actual)

def test_snoc_empy():
    expected = (1,)
    actual = snoc(1, [])
    assert_equal(expected, actual)

def test_snoc_none():
    expected = (1,)
    actual = snoc(1, None)
    assert_equal(expected, actual)

# take() tests

def test_take_happy():
    expected = (1,2,3)
    actual = take(3, (1,2,3,4,5))
    assert_equal(expected, actual)

def test_take_fewer_available():
    expected = (1,2)
    actual = take(3, (1,2))
    assert_equal(expected, actual)

def test_take_empty():
    expected = ()
    actual = take(3, ())
    assert_equal(expected, actual)

def test_take_from_none():
    expected = ()
    actual = take(3, None)
    assert_equal(expected, actual)

def test_take_zero():
    expected = ()
    actual = take(0, (1,2,3,4,5))
    assert_equal(expected, actual)

def test_take_neg():
    expected = ()
    actual = take(-3, (1,2,3,4,5))
    assert_equal(expected, actual)

def test_take_immutable():
    a = [1,2,3]
    expected = a
    take(3, a)
    actual = a
    assert_equal(expected, actual)

# take_end() tests

def test_take_end_happy():
    expected = (3,4,5)
    actual = take_end(3, (1,2,3,4,5))
    assert_equal(expected, actual)

def test_take_end_fewer_available():
    expected = (1,2)
    actual = take_end(3, (1,2))
    assert_equal(expected, actual)

def test_take_end_empty():
    expected = ()
    actual = take_end(3, ())
    assert_equal(expected, actual)

def test_take_end_from_none():
    expected = ()
    actual = take_end(3, None)
    assert_equal(expected, actual)

def test_take_end_zero():
    expected = ()
    actual = take_end(0, (1,2,3,4,5))
    assert_equal(expected, actual)

def test_take_end_neg():
    expected = ()
    actual = take_end(-3, (1,2,3,4,5))
    assert_equal(expected, actual)

def test_take_end_immutable():
    a = [1,2,3]
    expected = a
    take_end(3, a)
    actual = a
    assert_equal(expected, actual)

# drop() tests

def test_drop_happy():
    expected = (2,3)
    actual = drop(1, (1,2,3))
    assert_equal(expected, actual)

def test_drop_all():
    expected = ()
    actual = drop(3, (1,2,3))
    assert_equal(expected, actual)

def test_drop_more():
    expected = ()
    actual = drop(5, (1,2,3))
    assert_equal(expected, actual)

def test_drop_zero():
    expected = (1,2,3)
    actual = drop(0, (1,2,3))
    assert_equal(expected, actual)

def test_drop_negative():
    expected = (1,2,3)
    actual = drop(-3, (1,2,3))
    assert_equal(expected, actual)

def test_drop_from_none():
    expected = ()
    actual = drop(3, None)
    assert_equal(expected, actual)

def test_drop_immutable():
    a = [1,2,3]
    expected = a
    drop(3, a)
    actual = a
    assert_equal(expected, actual)

# drop_end() tests

def test_drop_end_happy():
    expected = (1,2)
    actual = drop_end(1, (1,2,3))
    assert_equal(expected, actual)

def test_drop_end_all():
    expected = ()
    actual = drop_end(3, (1,2,3))
    assert_equal(expected, actual)

def test_drop_end_more():
    expected = ()
    actual = drop_end(5, (1,2,3))
    assert_equal(expected, actual)

def test_drop_end_zero():
    expected = (1,2,3)
    actual = drop_end(0, (1,2,3))
    assert_equal(expected, actual)

def test_drop_end_negative():
    expected = (1,2,3)
    actual = drop_end(-3, (1,2,3))
    assert_equal(expected, actual)

def test_drop_end_from_none():
    expected = ()
    actual = drop_end(3, None)
    assert_equal(expected, actual)

def test_drop_end_immutable():
    a = [1,2,3]
    expected = a
    drop_end(3, a)
    actual = a
    assert_equal(expected, actual)

# nth() tests

def test_nth_happy():
    expected = 2
    actual = nth(1, (1,2,3))
    assert_equal(expected, actual)

def test_nth_0():
    expected = 1
    actual = nth(0, (1,2,3))
    assert_equal(expected, actual)

def test_nth_out_of_bounds():
    expected = None
    actual = nth(4, (1,2,3))
    assert_equal(expected, actual)

def test_nth_of_empty():
    expected = None
    actual = nth(1, ())
    assert_equal(expected, actual)

def test_nth_of_none():
    expected = None
    actual = nth(1, None)
    assert_equal(expected, actual)

def test_nth_neg():
    expected = None
    actual = nth(-1, (1,2,3))
    assert_equal(expected, actual)

# head() tests

def test_head_happy():
    expected = 1
    actual = head((1,2,3))
    assert_equal(expected, actual)

def test_head_empty():
    expected = None
    actual = head(())
    assert_equal(expected, actual)

def test_head_none():
    expected = None
    actual = head(None)
    assert_equal(expected, actual)

def test_head_immutable():
    a = [1,2,3]
    head(a)
    expected = a
    actual = a
    assert_equal(expected, actual)

# tail() tests

def test_tail_happy():
    expected = (2,3)
    actual = tail((1,2,3))
    assert_equal(expected, actual)

def test_tail_empty():
    expected = ()
    actual = tail(())
    assert_equal(expected, actual)

def test_tail_none():
    expected = ()
    actual = tail(None)
    assert_equal(expected, actual)

def test_tail_immutable():
    a = [1,2,3]
    tail(a)
    expected = a
    actual = a
    assert_equal(expected, actual)

# last() tests

def test_last_happy():
    expected = 3
    actual = last((1,2,3))
    assert_equal(expected, actual)

def test_last_empty():
    expected = None
    actual = last(())
    assert_equal(expected, actual)

def test_last_none():
    expected = None
    actual = last(None)
    assert_equal(expected, actual)

def test_last_immutable():
    a = [1,2,3]
    last(a)
    expected = a
    actual = a
    assert_equal(expected, actual)

# fold() tests

def test_fold_happy():
    expected = 6
    actual = fold(lambda x, y: x + y, (1,2,3), 0)
    assert_equal(expected, actual)

def test_fold_implicit_initial():
    expected = 6
    actual = fold(lambda x, y: (x or 0) + (y or 0), (1,2,3))
    assert_equal(expected, actual)

def test_fold_empty():
    expected = 0
    actual = fold(lambda x, y: x + y, [], 0)
    assert_equal(expected, actual)

def test_fold_none():
    expected = 0
    actual = fold(lambda x, y: x + y, None, 0)
    assert_equal(expected, actual)

# concat() tests

def test_concat_happy():
    expected = (1,2,3,4,5,6)
    actual = concat(((1,2,3), (4,5,6)))
    assert_equal(expected, actual)

def test_concat_strings():
    expected = ("hello", "world")
    actual = concat(("hello", "world"))
    assert_equal(expected, actual)

# flatten() tests

def test_flatten_happy():
    expected = (1,2,3,4)
    actual = flatten([(1,2), 3, [[4]]])
    assert_equal(expected, actual)

def test_flatten_none():
    expected = ()
    actual = flatten(None)
    assert_equal(expected, actual)

def test_flatten_scalar():
    expected = (1,)
    actual = flatten(1)
    assert_equal(expected, actual)

def test_flatten_string():
    expected = ("hi!",)
    actual = flatten("hi!")
    assert_equal(expected, actual)

def test_flatten_bytes():
    expected = (b"hi!",)
    actual = flatten(b"hi!")
    assert_equal(expected, actual)

def test_flatten_dict():
    expected = ("hi!",)
    actual = flatten({"foo":"hi!"})
    assert_equal(expected, actual)

# cat_maybes test

def test_cat_maybes():
    expected = (1,2,3,4)
    actual = cat_maybes((1,2,None,3,None,None,4,None))
    assert_equal(expected, actual)

# prop() tests

def test_prop_happy():
    expected = 1
    actual = prop('foo', {'bar': 2, 'foo': 1})
    assert_equal(expected, actual)

# path() tests

def test_path_happy():
    expected = 1
    actual = path(['foo', 'bar'], {'foo': {'bar': 1}})
    assert_equal(expected, actual)

def test_path_notfound():
    expected = None
    actual = path(['baz', 'bar'], {'foo': {'bar': 1}})
    assert_equal(expected, actual)

# assoc_path() tests

def test_assoc_path_happy():
    expected = {'foo': {'bar': 1}}
    actual = assoc_path(['foo', 'bar'], 1, {'foo': {'bar': 3}})
    assert_equal(expected, actual)

def test_assoc_path_simple_on_empty():
    expected = {'foo': 1}
    actual = assoc_path(['foo'], 1, {})
    assert_equal(expected, actual)

def test_assoc_path_on_empty():
    expected = {'foo': {'bar': 1}}
    actual = assoc_path(('foo', 'bar'), 1, {})
    assert_equal(expected, actual)

def test_assoc_path_on_none():
    expected = {'foo': {'bar': 1}}
    actual = assoc_path(('foo', 'bar'), 1, None)
    assert_equal(expected, actual)

# prop_lens tests

def test_prop_lens_get():
    lens = prop_lens("foo")
    data = {"foo": "bar", "baz": "quux"}
    expected = "bar"
    actual = Lens.get(lens, data)
    assert_equal(expected, actual)

def test_prop_lens_set():
    lens = prop_lens("foo")
    data = {"baz": "quux"}
    expected = {"foo": "bar", "baz": "quux"}
    actual = Lens.set(lens, "bar", data)
    assert_equal(expected, actual)

def test_prop_lens_set_empty():
    lens = prop_lens("foo")
    data = {}
    expected = {"foo": "bar"}
    actual = Lens.set(lens, "bar", data)
    assert_equal(expected, actual)

def test_prop_lens_set_none():
    lens = prop_lens("foo")
    data = None
    expected = {"foo": "bar"}
    actual = Lens.set(lens, "bar", data)
    assert_equal(expected, actual)

def test_prop_lens_over():
    lens = prop_lens("foo")
    data = {"foo": "bar", "baz": "quux"}
    expected = {"foo": "BAR", "baz": "quux"}
    actual = Lens.over(lens, lambda x: x.upper(), data)
    assert_equal(expected, actual)

def test_prop_lens_over_nonexistent():
    lens = prop_lens("foo")
    data = {"baz": "quux"}
    expected = {"baz": "quux"}
    actual = Lens.over(lens, lambda x: x.upper(), data)
    assert_equal(expected, actual)

def test_prop_lens_overwrite():
    lens = prop_lens("foo")
    data = {"foo": "canary", "baz": "quux"}
    expected = {"foo": "bar", "baz": "quux"}
    actual = Lens.set(lens, "bar", data)
    assert_equal(expected, actual)

def test_prop_lens_set_immutable():
    lens = prop_lens("foo")
    data = {"baz": "quux"}
    expected = {"baz": "quux"}
    Lens.set(lens, "bar", data)
    actual = data
    assert_equal(expected, actual)

# compose_lens test

def test_composed_lens_get():
    lens = compose_lens(prop_lens("foo"), prop_lens("bar"))
    data = {"foo": {"bar": "baz"}}
    expected = "baz"
    actual = Lens.get(lens, data)
    assert_equal(expected, actual)

def test_composed_lens_set():
    lens = compose_lens(prop_lens("foo"), prop_lens("bar"))
    data = {"foo": {"bar": "baz"}}
    expected = {"foo": {"bar": "quux"}}
    actual = Lens.set(lens, "quux", data)
    assert_equal(expected, actual)

def test_composed_lens_over():
    lens = compose_lens(prop_lens("foo"), prop_lens("bar"))
    data = {"foo": {"bar": "baz"}}
    expected = {"foo": {"bar": "BAZ"}}
    actual = Lens.over(lens, lambda x: x.upper(), data)
    assert_equal(expected, actual)

# path_lens tests

def test_path_lens_get_variadic():
    lens = path_lens("foo", "bar")
    data = {"foo": {"bar": "baz"}}
    expected = "baz"
    actual = Lens.get(lens, data)
    assert_equal(expected, actual)

def test_path_lens_get_mixed():
    lens = path_lens("foo", prop_lens("bar"))
    data = {"foo": {"bar": "baz"}}
    expected = "baz"
    actual = Lens.get(lens, data)
    assert_equal(expected, actual)

def test_path_lens_get_list():
    lens = path_lens(["foo", "bar"])
    data = {"foo": {"bar": "baz"}}
    expected = "baz"
    actual = Lens.get(lens, data)
    assert_equal(expected, actual)

def test_path_lens_get_nested():
    lens = path_lens(("foo", ("bar",)))
    data = {"foo": {"bar": "baz"}}
    expected = "baz"
    actual = Lens.get(lens, data)
    assert_equal(expected, actual)

def test_path_lens_set():
    lens = path_lens("foo", "bar")
    data = {"foo": {"bar": "baz"}}
    expected = {"foo": {"bar": "quux"}}
    actual = Lens.set(lens, "quux", data)
    assert_equal(expected, actual)

def test_path_lens_set_empty():
    lens = path_lens(["foo", "bar"])
    expected = {"foo": {"bar": "quux"}}
    actual = Lens.set(lens, "quux", {})
    assert_equal(expected, actual)

def test_path_lens_over():
    lens = path_lens("foo", "bar")
    data = {"foo": {"bar": "baz"}}
    expected = {"foo": {"bar": "BAZ"}}
    actual = Lens.over(lens, lambda x: x.upper(), data)
    assert_equal(expected, actual)
