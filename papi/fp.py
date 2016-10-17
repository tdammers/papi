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

def assoc(key, val, obj=None):
    new_obj = {} if obj is None else dict(obj)
    new_obj[key] = val
    return new_obj

def assocs(keyvals, obj=None):
    new_obj = obj
    for k,v in keyvals:
        new_obj = assoc(k, v, new_obj)
    return new_obj

def dissoc(key, obj):
    new_obj = dict(obj)
    new_obj.pop(key)
    return new_obj

def _tuplize(t):
    return () if t is None else tuple(t)

def cons(h, t=None):
    return (h,) + _tuplize(t)

def snoc(h, t=None):
    return _tuplize(t) + (h,)

def take(n, t):
    if n <= 0:
        return ()
    return _tuplize(t)[0:n]

def drop(n, t):
    if n <= 0:
        return _tuplize(t)
    return _tuplize(t)[n:]

def nth(n, t=None):
    if t is None:
        return None
    n = int(n)
    if n < 0:
        return None
    try:
        return t[n]
    except IndexError:
        return None

def head(t):
    return nth(0, t)

def tail(t):
    return drop(1, t)

def fold(func, items, initial=None):
    accum = initial
    for item in _tuplize(items):
        accum = func(accum, item)
    return accum
