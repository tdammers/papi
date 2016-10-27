def assert_equal(expected, actual, test_name=None):
    if expected == actual:
        return
    expected_str = repr(expected)
    actual_str = repr(actual)
    if len(expected_str) > 50 or len(actual_str) > 50:
        msg = "assert_equal:\n\texpected:\n\t{0}\n\tbut found:\n\t{1}".format(
            repr(expected), repr(actual))
    else:
        msg = "assert_equal: expected {0}, but found {1}".format(
            repr(expected), repr(actual))
    if test_name is not None:
        msg += " in test '{0}'".format(test_name)
    raise AssertionError(msg)


