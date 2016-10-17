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
    return _tuplize(t)[:n]

def drop(n, t):
    if n <= 0:
        return _tuplize(t)
    return _tuplize(t)[n:]

def drop_end(n, t):
    if n <= 0:
        return _tuplize(t)
    return _tuplize(t)[:-n]

def take_end(n, t):
    if n <= 0:
        return ()
    return _tuplize(t)[-n:]

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

def last(t):
    return nth(len(t) - 1, t)

def tail(t):
    return drop(1, t)

def fold(func, items, initial=None):
    accum = initial
    for item in _tuplize(items):
        accum = func(accum, item)
    return accum

def concat(items):
    return fold(lambda x, y: x + y, items, ())

def flatten(items):
    # special case for strings and bytestrings:
    if isinstance(items, str):
        return (items,)
    if isinstance(items, bytes):
        return (items,)
    # if it's iterable, turn it into a flat tuple:
    if hasattr(items, '__iter__'):
        return tuple(concat(map(flatten, items)))
    # if it's neither of the above, assume it's scalar, wrap it in a 1-tuple.
    return (items,)

def prop(p, item):
    return prop_lens(p).get(item)

def path(p, item):
    return path_lens(p).get(item)

def assoc_path(p, value, item):
    return path_lens(p).set(value, item)

def compose(f1, f2):
    def f(*args, **kwargs):
        return f1(f2(*args, **kwargs))
    return f

def identity(x, *args, **kwargs):
    return x

def rcompose(f1, f2):
    return compose(f2, f1)

def chain(*fns):
    if len(fns) == 0:
        return identity
    return fold(compose, tail(fns), head(fns))

def dictmap(f, item):
    return dict((k, f(v)) for k, v in item.items())

class Lens(object):
    """A Lens abstracts over a getter/setter pair and represents a "view" on
    a data object.

    Lens Law:

    lens.get(lens.set(value, subject)) == value

    Informally: setting the target of a lens produces an object for which
    getting the target of the same lens will return the value passed to the
    setter.

    Even more informally: lenses behave like properties, lens.get() being the
    analog of dict.get(), and lens.put() the analog of dict.__setitem__().

    Lenses are composable: see the compose_lens() function for a primitive
    lens combinator.
    """
    def __init__(self, getter, setter):
        self.getter = getter
        self.setter = setter

    def get(self, subject):
        """Apply the lens' getter to the subject.
        """
        return self.getter(subject)

    def set(self, value, subject):
        """Apply the lens' setter to the subject.
        """
        return self.setter(value, subject)

    def over(self, f, subject):
        """Modify the target of the lens by applying the given function "f" to it.
        """
        value = self.get(subject)
        if value is None:
            return subject
        return self.set(f(value), subject)

def prop_lens(prop_name):
    """Create a Lens that drills down into a dict-like object's named property.
    """
    def getter(subject):
        return subject.get(prop_name)
    def setter(value, subject):
        return assoc(prop_name, value, subject)
    return Lens(getter, setter)

def path_lens(*path):
    """Create a Lens that follows a path of properties.
    The path can be passed as variable positional args, or as any iterable, or
    any combination thereof, so the following are all equivalent:

    path_lens("foo", "bar", "baz")
    path_lens(["foo", "bar", "baz"])
    path_lens("foo", ["bar", "baz"])
    path_lens(("foo", ("bar", ("baz"))))

    Caveat: some collection types are iterable despite not having a defined
    ordering. Using such types in your path will cause unpredictable behavior,
    because the ordering of path segments cannot be guaranteed. For example:

    path_lens(set(("foo", "bar")))

    ...could produce either foo -> bar or bar -> foo, depending on which
    ordering the set happens to produce. So, uhm, don't do that OK?

    For extra convenience, any of the individual path items can be a lens
    instead of a prop name, which allows you to splice existing lenses into the
    path:

    path_lens("foo", some_lens, "bar")

    This also means that path_lens can act as a generic variadic lens composer
    function, and the following are equivalent:

    path_lens(lens1, lens2, lens3)
    compose_lens(lens1, compose_lens(lens2, lens3))

    """
    path = flatten(path)
    def to_lens(item):
        if isinstance(item, Lens):
            return item
        else:
            return prop_lens(item)
    return fold(
        compose_lens,
        map(to_lens, path),
        identity_lens())

def compose_lens(left, right):
    """Compose lenses outer-to-inner.
    The following are equivalent:
        get(compose_lens(left, right), subject) == get(left, get(right, subject))
    """
    def getter(subject):
        return right.get(left.get(subject))
    def setter(value, subject):
        return left.over(lambda inner: right.set(value, inner), subject)
    return Lens(getter, setter)

def identity_lens():
    """Create a no-op lens that operates on the subject itself. Note, however,
    that .set() is still pure, meaning that it will not modify the subject;
    instead, it will just return the value passed to it and not touch the
    subject at all.
    """
    def getter(subject):
        return subject
    def setter(value, subject):
        return value
    return Lens(getter, setter)
