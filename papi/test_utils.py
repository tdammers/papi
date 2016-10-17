def assert_equal(expected, actual, test_name=None):
    if expected == actual:
        return
    msg = "assert_equal: expected {0}, but found {1}".format(
        repr(expected), repr(actual))
    if test_name is not None:
        msg += " in test '{0}'".format(test_name)
    raise AssertionError(msg)


