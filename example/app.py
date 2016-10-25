import logging
import json
from papi.serve import serve_resource
import papi.fp as fp
from papi.mime import match_mime, parse_mime_type
from papi.exceptions import ResourceException
import random
import string

logger = logging.getLogger(__name__)

text_plain_utf8 = parse_mime_type("text/plain;charset=utf8")
text_plain_any = parse_mime_type("text/plain")

class DictResource(object):
    def __init__(self, data=None, children=None):
        self.data = data or {}
        self.children = None if children is None else dict(children)

    def get_structured_body(self, **kwargs):
        return self.data

    def get_typed_body(self, mime_pattern):
        if isinstance(self.data, str):
            if match_mime(mime_pattern, text_plain_utf8, ["charset"]):
                return (text_plain_utf8, self.data)
        return None

    def get_children(self, *args, **kwargs):
        if self.children is None:
            return None
        return sorted(self.children.items())

    def get_child(self, name):
        print("Get child: {0}".format(name))
        if self.children is None:
            return None
        return self.children.get(name)

    def parse_body(self, input, content_type=None):
        print(content_type)
        if match_mime(text_plain_any, content_type):
            print("MATCH")
            raw_body = input.read()
            charset = content_type.props.get('charset', 'ascii')
            body = raw_body.decode(charset)
            return body
        else:
            raise ResourceException(ResourceException.reason_wrong_type)

    def create(self, input, content_type=None):
        def make_token():
            alphabet = string.ascii_letters + string.digits
            return ''.join((random.choice(alphabet) for _ in range(0, 16)))

        body = self.parse_body(input, content_type)
        base_name = (fp.head(body.split()) or "unnamed").lower()
        name = base_name
        while name in self.children:
            if base_name == "":
                name = make_token()
            else:
                name = make_token() + "-" + base_name
        self.children[name] = DictResource(body)
        return name, body

    def store(self, input, name, content_type=None):
        body = self.parse_body(input, content_type)
        self.children[name] = DictResource(body)
        return name, body

    def delete(self, name):
        if name in self.children:
            del self.children[name]
            return True
        else:
            return False

raw_things = {
    'apple': "I am an apple. Eat me.",
    'onion': "Hurt me, and I will make you cry.",
    'banana': "I'll bend either way for you.",
    'nut': "I'm nuts!"
}
things = fp.dictmap(DictResource, raw_things)
root = DictResource(
    children={
        'things': DictResource(children=things)
    })

application = serve_resource(root)
