from papi.fp import *

def assert_equal(expected, actual, test_name=None):
    if expected == actual:
        return
    msg = "assert_equal: expected {0}, but found {1}".format(
        repr(expected), repr(actual))
    if test_name is not None:
        msg += " in test '{0}'".format(test_name)
    raise AssertionError(msg)

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
