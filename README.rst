papi
====

Low-Boilerplate RESTful APIs
----------------------------

Introduction
------------

papi is a library that allows you to build powerful
`RESTful <https://en.wikipedia.org/wiki/Restful>`__ web services on top
of plain WSGI by writing backends as simple and semantic classes, and
then feeding them to its equally simple WSGI wrapper function.

Features
--------

-  Proper RESTful semantics over HTTP(S): GET, PUT, POST, DELETE map to
   retrieve / list resources, create, update, delete
-  Automatic routing
-  Automatic `HATEOAS <https://en.wikipedia.org/wiki/HATEOAS>`__
   decoration (adds links to parent, self, and children, on every JSON
   response)
-  Semi-automatic content type negotiation: JSON is handled
   transparently, other content types are easy to support in your
   backend code
-  Automatic translations of failures to HTTP error responses; uses the
   4xx range of status codes correctly
-  Runs on any compliant WSGI host, making it suitable for deployment
   under a wide range of web servers and protocols
-  Method override: fake unsupported HTTP methods through GET parameters
   or headers

Installing
----------

Installing with pip:

.. code:: bash

    pip install papi

You probably want to do this in a virtualenv.

Conceptual Model
----------------

Papi's concept of a RESTful API is that of a tree-shaped data structure,
consisting of "leaf" nodes called "documents" and "branch" nodes called
"collections". Both are modelled as *resources*, and a resource can act
as a document, as a collection, or both. Documents have a body
(potentially available in multiple flavors, matching different MIME
content types); collections have child resources, and the library code
maps this resource tree onto a URL path structure. As RESTfulness has
it, HTTP methods indicate the kind of operation on this tree, and the
HATEOAS philosophy is applied by tagging documents and collections with
metadata when possible.

Usage
-----

Defining A Resource
~~~~~~~~~~~~~~~~~~~

To implement a working RESTful API, you need to define a root resource.
Resources can act as documents (having a body), collections (having
child resources), or hybrids (having both a body and child resources).
For the root resource, you almost certainly want a collection-style
resource, otherwise your API will only ever contain one document.

    Note that ``Resource`` is not a base class, it's just an implicit
    interface. Papi resolves method calls through duck typing, there is
    no need to inherit or formally implement anything, just add the
    methods you need, and that's it. Adding other methods is of course no
    problem at all.

The relevant methods for a resource are:

.. code:: python

    def get_structured_body(self, digest=False)
    def get_typed_body(self, mime_pattern)

Get the payload data for the resource itself; implementing these methods
makes the resource a document.

``get_typed_body`` is always tried first; it should return a pair of
``(mime_type, body)`` to indicate that a body is available that matches
the ``mime_pattern``, or ``None`` to tell Papi that this MIME type
cannot be satisfied.

For some "special" MIME types (currently only ``text/json`` and
``application/json``), the ``get_structured_body`` method is tried when
``get_typed_body`` fails; this method is supposed to return a native
Python data structure. Currently, the only requirement is that the
returned data must be JSON-encodable, but in the future, other types may
be supported (e.g. XML, plain text, HTML, ...), so it's best to stick
with "vanilla" data structures that directly correspond to JSON types:
``dict``, ``list``, ``tuple``, ``int``, ``float``, ``bool``, ``str`` and
``None`` are all safe to use, others might not. The ``digest`` argument
indicates whether the full body should be returned, or a "digest"
version that contains only the essential properties. ``digest`` will be
``True`` when called on a child resource in a collection listing
context, ``False`` when the resource is requested directly.

    One thing to keep in mind with these two methods is that **documents
    derived from ``get_typed_body`` are never parsed, and no metadata is
    ever added**.  This means that if you want to have Papi add HATEOAS
    links and a list of child resources to the response, you must
    implement ``get_structured_body``, and if you also implement
    ``get_typed_body``, it must return ``None`` for at least the JSON
    content types (and, in the future, any content type you want to have
    tagged with metadata).

.. code:: python

    def get_children(self, offset=0, count=10, filters=None, order=None)
    def get_child(self, name)

These methods need to be implemented for resources that act as
collections. ``get_children`` returns a list of ``(name, resource)``
pairs, and can take the following keyword arguments to alter its behavior:

-  ``filters``: a list of ``Filter`` objects. A ``Filter`` object has three
   properties: ``operator``, ``value``, and ``propname``, where ``propname``
   indicates which property of the document to compare, ``operator`` indicates
   how to compare (currently only ``"equals"`` is used), and ``value`` is a
   (string) value that the property is compared against.
- ``order``: a list of ``(descending, order-key)`` pairs, from most-significant
   to least-significant. If ``descending`` is ``True``, the result must be
   ordered in descending order. ``order-key`` is specific to the resource, no
   further interpretation is performed by Papi.
-  ``offset``: the number of items to skip from the beginning of the
   list. Works like Python's ``x[offset:]`` construct, or the ``OFFSET``
   part in an SQL ``LIMIT`` clause.
-  ``count``: the number of items to return, starting at the ``offset``
   if provided. Works like Python's ``x[:count]`` construct, or the
   ``COUNT`` part in an SQL ``LIMIT`` clause.
-  ``page``: when ``count`` is specified, you can provide a page number
   instead of an ``offset``. Page numbers are 1-based, and each page
   contains ``count`` entries, so ``page=2, count=10`` retrieves items
   10 through 19.

It is recommended to implement ``get_children`` with additional ``*args`` and
``**kwargs`` arguments, such that future Papi versions can add additional
arguments without breaking compatibility.

``get_child`` gets a single child resource; the ``name`` parameter,
throughout Papi's Python API, refers to a resource's primary key. We
call it "name", because ideally, it should be a somewhat descriptive,
meaningful natural identifier for the object it represents, which, when
possible, is more in line with the RESTful philosophy, and makes for
naturally beautiful URIs.
``http://example.org/api/fruit/apples/granny_smith`` is a much nicer URI
than ``http://example.org/api/5d75e3/35b0bd/d68c481bb1f4``.

.. code:: python

    def create(self, input, content_type=None)
    def store(self, input, name, content_type=None)
    def delete(self, name)

These methods can optionally be implemented to turn a readonly resource
into a writeable collection. Note that *all* write operations are
defined on the parent resource, even though at the HTTP level, some are
exposed on the resource itself - for example, ``POST /root/child1`` maps
to the resource named ``"child1"`` under the parent resource ``"root"``,
but the method that gets called is the ``store`` method of the ``root``
resource. This is for two reasons: one, the child resource to store may
not exist yet (this is the case for ``PUT`` requests), and two, the
resource itself does not know its own name, nor does it need to.

Some notes on these methods:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``input`` argument will contain a file-like object, which means
you can use the usual ``read()`` etc. methods on it to extract the
body. Parsing is your own responsibility, Papi does not do this for
you. Particularly, there is no write equivalent to the
``get_structured_body`` method; however, processing JSON documents is
usually a simple matter of calling ``json.loads``.

The difference between ``create`` and ``store`` is that ``create``
must generate a name for the received document, and return a
``name, body`` tuple (where ``body`` is a digest that describes the
document that has been created, in a JSON-encodable data structure
according to the same rules as ``get_structured_body``); multiple
calls to ``create`` should create multiple distinct documents, and
return distinct names. Conceptually, ``create`` *always* creates a
new document. By contrast, ``store`` takes a document name as an
argument, so it does not generate one itself, and multiple calls with
the same name will overwrite one another. While ``store`` may also
create new documents (if the ``name`` does not exist yet), it should
overwrite (update) documents when the name already exists.

Serving A Resource
~~~~~~~~~~~~~~~~~~

Serving a resource is simple; the ``serve_resource`` function can be
used to turn a valid resource into a WSGI application, like this:

.. code:: python

    application = serve_resource(root_resource)

And from there, it's a matter of feeding that function to a WSGI server
(see the `WSGI documentation <https://wsgi.readthedocs.io/en/latest/>`__
for details).

Give It A Spin
~~~~~~~~~~~~~~

The included example application (``example/app.py``) implements a
simple in-memory database that supports plain-text payloads for
documents; all the resources in it are read/write document/collection
hybrids, which means that data can be added at any point in the tree.
Assuming that this application runs in a WSGI server on localhost:5000,
we can try a few requests (we'll use cURL for these examples):

.. code:: bash

    > curl 'http://localhost:5000/' # Fetch the root resource

    {"_parent": {"href": "/"}, "_self": {"href": "/"}, "_items": [{"_parent":
    {"href": "/"}, "_self": {"href": "/things"}, "_name": "things"}]}

That's not very readable, but we can use the ``pretty`` parameter to
pretty-print JSON output:

.. code:: bash

    > curl 'http://localhost:5000/?pretty=1'
    {
      "_parent": {
        "href": "/"
      },
      "_self": {
        "href": "/"
      },
      "_items": [
        {
          "_parent": {
            "href": "/"
          },
          "_self": {
            "href": "/things"
          },
          "_name": "things"
        }
      ]
    }

This tells us a few things:

-  The URI for this resource (``_self``) is ``/``
-  The URI for this resource's parent (``_parent``) is also '/' (this is
   actually a misfeature currently; the root node should not actually
   report a parent)
-  The resource contains child resources (``_items``)
-  To be specific, it contains *one* child resource, named ``things``,
   with a URI of ``/things``.

As you can see, this HATEOAS metadata makes the API fully discoverable;
the resource tells us its own location within the API, as well as those
of its parent and children.

Let's look at the child resource "things":

.. code:: bash

    > curl 'http://localhost:5000/things/?pretty=1'
    {
      "_parent": {
        "href": "/"
      },
      "_self": {
        "href": "/things"
      },
      "_items": [
        {
          "_parent": {
            "href": "/things"
          },
          "_self": {
            "href": "/things/apple"
          },
          "_value": "I am an apple. Eat me.",
          "_name": "apple"
        },
        {
          "_parent": {
            "href": "/things"
          },
          "_self": {
            "href": "/things/banana"
          },
          "_value": "I'll bend either way for you.",
          "_name": "banana"
        },
        {
          "_parent": {
            "href": "/things"
          },
          "_self": {
            "href": "/things/nut"
          },
          "_value": "I'm nuts!",
          "_name": "nut"
        },
        {
          "_parent": {
            "href": "/things"
          },
          "_self": {
            "href": "/things/onion"
          },
          "_value": "Hurt me, and I will make you cry.",
          "_name": "onion"
        }
      ],
      "_name": "things"
    }

Oh joy! What a bunch of things! And they're still fully
HATEOAS-discoverable, so let's see what happens when we try to fetch an
onion:

.. code:: bash

    > curl 'http://localhost:5000/things/onion/?pretty=1'
    Hurt me, and I will make you cry.

That's weird. No JSON. Why is that? Right, content negotiation. Our
example resource supports ``text/plain`` as well as JSON; curl, by
default, specifies that it accepts ``*/*``, that is, *anything*, and
because Papi prefers "typed" bodies over "structured" bodies, the first
type that matches (which happens to be ``text/plain``) is what we get.
If we were serving, say, images through our API, this would be *exactly*
the desired behavior. We can still request JSON though, we just have to
override the ``Accept`` header:

.. code:: bash

    > curl 'http://localhost:5000/things/onion/?pretty=1' -H 'Accept: text/json'
    {
      "_parent": {
        "href": "/things"
      },
      "_self": {
        "href": "/things/onion"
      },
      "_value": "Hurt me, and I will make you cry.",
      "_name": "onion"
    }

All is well!

So far, we have only requested things that existed. Of course requesting
something that doesn't exist yields a 404 error; we'll use cURL's ``-i``
option to show HTTP headers:

.. code:: bash

    > curl 'http://localhost:5000/things/nope/?pretty=1' -i
    HTTP/1.1 404 Not Found
    Content-type: text/plain;charset=utf8

    Not Found

That makes sense.

What happens if we request a content type that the resource doesn't
support?

.. code:: bash

    > curl 'http://localhost:5000/things/onion/?pretty=1' -i -H 'Accept: img/png'
    HTTP/1.1 406 Not Acceptable
    Content-type: text/plain;charset=utf8

    Not Acceptable

It does the right thing.

So far we've only been *reading* from the API; let's try *writing*
things. According to standard RESTful procedures, we can create new
documents by using the HTTP ``PUT`` method:

.. code:: bash

    > curl 'http://localhost:5000/things/potato' -XPUT -i -H 'Content-Type: text/plain'
    HTTP/1.1 200 OK
    Content-type: application/json

    {"_parent": {"href": "/things"}, "_self": {"href": "/things/potato"}, "_value": "Slice me, dice me, fry me"}

The status code ``200`` indicates that the document was indeed created,
and fetching the ``_self`` URI confirms this:

.. code:: bash

    > curl 'http://localhost:5000/things/potato/?pretty=1'
    Slice me, dice me, fry me

And of course, this new document supports JSON as well:

.. code:: bash

    > curl 'http://localhost:5000/things/potato/?pretty=1' -H 'Accept: text/json'
    {
      "_parent": {
        "href": "/things"
      },
      "_self": {
        "href": "/things/potato"
      },
      "_value": "Slice me, dice me, fry me",
      "_name": "potato"
    }

Note that if you want to access the API from a web browser, it will
almost certainly not support any HTTP methods other than ``GET`` and
``POST`` (plus a few that we don't care much about here, such as
``HEAD`` and ``OPTIONS``); ``PUT`` and ``DELETE``, in particular, will
not work. Because of this, Papi has a method override feature: if you
add a ``_method`` parameter to the query string, or a
``X-Method-Override`` header to the request, the value of that will
override the actual request method. So the following curl requests would
all produce the same behavior:

.. code:: bash

    > curl 'http://localhost:5000/things/potato' -XPUT -i -H 'Content-Type: text/plain'
    > curl 'http://localhost:5000/things/potato?_method=PUT' -XPOST -i -H 'Content-Type: text/plain'
    > curl 'http://localhost:5000/things/potato' -XPOST -i -H 'X-Method-Override: PUT' -H 'Content-Type: text/plain'

An alternative way of creating new documents is using the HTTP method
``POST`` on the *parent* resource, leaving the responsibility of
generating a suitable unique name for the new document to the parent
resource. This is what that looks like:

.. code:: bash

    > curl 'http://localhost:5000/things?pretty=1' -XPOST -i -H 'Content-Type: text/plain' -d'Carrot on a stick'
    HTTP/1.1 200 OK
    Content-type: application/json

    {"_parent": {"href": "/things"}, "_self": {"href": "/things/carrot"}, "_value": "Carrot on a stick"}

Our example resource is configured to generate names based on the first
word of the input, so that's what we get: ``"carrot"``.

Other than the ``PUT`` method, however, ``POST`` will always create a
new document, rather than overwrite an existing one, so if we ``POST``
the same thing again, the API is required to either deny the request
with a ``Conflict`` response, or create a new document with a different
unique name. Our example application opts for the second solution:

.. code:: bash

    > curl 'http://localhost:5000/things?pretty=1' -XPOST -i -H 'Content-Type: text/plain' -d'Carrot on a stick'
    HTTP/1.1 200 OK
    Content-type: application/json

    {"_parent": {"href": "/things"}, "_self": {"href": "/things/BL6yCijd8x4Mwzcf-carrot"}, "_value": "Carrot on a stick"}

As you can see, the name is disambiguated by prepending a random token.
Listing the ``/things`` resource shows that two documents have actually
been created:

.. code:: bash

    > curl 'http://localhost:5000/things?pretty=1' -H 'Accept: text/json'
    {
      "_parent": {
        "href": "/"
      },
      "_self": {
        "href": "/things"
      },
      "_items": [
        {
          "_parent": {
            "href": "/things"
          },
          "_self": {
            "href": "/things/BL6yCijd8x4Mwzcf-carrot"
          },
          "_value": "Carrot on a stick",
          "_name": "BL6yCijd8x4Mwzcf-carrot"
        },
        {
          "_parent": {
            "href": "/things"
          },
          "_self": {
            "href": "/things/apple"
          },
          "_value": "I am an apple. Eat me.",
          "_name": "apple"
        },
        {
          "_parent": {
            "href": "/things"
          },
          "_self": {
            "href": "/things/banana"
          },
          "_value": "I'll bend either way for you.",
          "_name": "banana"
        },
        {
          "_parent": {
            "href": "/things"
          },
          "_self": {
            "href": "/things/carrot"
          },
          "_value": "Carrot on a stick",
          "_name": "carrot"
        },
        {
          "_parent": {
            "href": "/things"
          },
          "_self": {
            "href": "/things/nut"
          },
          "_value": "I'm nuts!",
          "_name": "nut"
        },
        {
          "_parent": {
            "href": "/things"
          },
          "_self": {
            "href": "/things/onion"
          },
          "_value": "Hurt me, and I will make you cry.",
          "_name": "onion"
        },
        {
          "_parent": {
            "href": "/things"
          },
          "_self": {
            "href": "/things/potato"
          },
          "_value": "Slice me, dice me, fry me",
          "_name": "potato"
        }
      ],
      "_name": "things"
    }

And of course our example application also supports deleting items,
using the ``DELETE`` method:

.. code:: bash

    > curl 'http://localhost:5000/things/potato/?pretty=1' -i -XDELETE
    HTTP/1.1 204 No Content
    Content-type: text/plain

Note the use of the ``204 No Content`` status line; since we've deleted
a resource, there is no meaningful content to return, all we get is an
empty success response. And to confirm that the potato has indeed been
deleted:

.. code:: bash

    > curl 'http://localhost:5000/things?pretty=1' -H 'Accept: text/json'
    {
      "_parent": {
        "href": "/"
      },
      "_self": {
        "href": "/things"
      },
      "_items": [
        {
          "_parent": {
            "href": "/things"
          },
          "_self": {
            "href": "/things/BL6yCijd8x4Mwzcf-carrot"
          },
          "_value": "Carrot on a stick",
          "_name": "BL6yCijd8x4Mwzcf-carrot"
        },
        {
          "_parent": {
            "href": "/things"
          },
          "_self": {
            "href": "/things/apple"
          },
          "_value": "I am an apple. Eat me.",
          "_name": "apple"
        },
        {
          "_parent": {
            "href": "/things"
          },
          "_self": {
            "href": "/things/banana"
          },
          "_value": "I'll bend either way for you.",
          "_name": "banana"
        },
        {
          "_parent": {
            "href": "/things"
          },
          "_self": {
            "href": "/things/carrot"
          },
          "_value": "Carrot on a stick",
          "_name": "carrot"
        },
        {
          "_parent": {
            "href": "/things"
          },
          "_self": {
            "href": "/things/nut"
          },
          "_value": "I'm nuts!",
          "_name": "nut"
        },
        {
          "_parent": {
            "href": "/things"
          },
          "_self": {
            "href": "/things/onion"
          },
          "_value": "Hurt me, and I will make you cry.",
          "_name": "onion"
        }
      ],
      "_name": "things"
    }
