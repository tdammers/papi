def fmap(f, d):
    """ A generalized "map()", similar to the "fmap" function in Haskell.
    Applies the function "f" in the functor "d". For the purposes of this
    function, the following things are considered functors:
    - Dictionary-like objects (anything that has an .items() function); here,
      "f" is applied to the values, keeping the keys and key-value relationships
      intact.
    - Iterables; "f" is applied to all the values, ordering is kept intact.
    - Functions; returns a new function that passes its arguments to "d" and
      then applied "f" to the return value.
    - Anything else is considered an option, "f" is applied if "d" is not None.
    """
    if hasattr(d, "items") and callable(d.items):
        return dict( ( (k, f(v)) for k, v in d.items() ) )
    elif hasattr(d, "__iter__"):
        return map(f, d)
    elif callable(d):
        def wrapped(*args, **kwargs):
            retval = d(*args, **kwargs)
            if retval is None:
                return None
            else:
                return f(retval)
    elif d is None:
        return None
    else:
        return f(d)
