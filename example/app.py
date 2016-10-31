import logging
import json
from papi.serve import serve_resource
import papi.fp as fp
from papi.mime import match_mime, parse_mime_type
from papi.exceptions import ResourceException
import random
import string
from functools import partial

logger = logging.getLogger(__name__)

text_plain_utf8 = parse_mime_type("text/plain;charset=utf8")
text_plain_any = parse_mime_type("text/plain")
text_json_any = parse_mime_type("text/json")
application_json = parse_mime_type("application/json")

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

    def get_children(self, offset=None, count=20, page=None, filters=None):
        if self.children is None:
            return None
        if count is None or count == '':
            count = 20
        else:
            count = int(count)
        if offset is None or offset == '':
            if page is None or page == '':
                page = 1
            else:
                page = int(page)
            offset = (page - 1) * count
        else:
            offset = int(offset)
        print(count, offset)

        def apply_filter(f, target):
            compare_funcs = {
                'equals': lambda x, y: x == y,
            }

            compare_func = compare_funcs.get(f.operator)
            if compare_func is None:
                return False
            comparee = target if type(target) is dict else {"_value": target}
            return compare_func(f.value, fp.prop(f.propname, comparee))
            
        def apply_filters(target):
            for f in (filters or []):
                if not apply_filter(f, target[1]):
                    return False
            return True

        return fp.chain(
            partial(fp.take, count),
            partial(fp.drop, offset),
            sorted,
            partial(filter, apply_filters))(self.children.items())

    def get_child(self, name):
        print("Get child: {0}".format(name))
        if self.children is None:
            return None
        return self.children.get(name)

    def parse_body(self, input, content_type=None):
        print(content_type)
        if match_mime(text_plain_any, content_type):
            raw_body = input.read()
            charset = content_type.props.get('charset', 'ascii')
            body = raw_body.decode(charset)
            return body
        elif match_mime(text_json_any, content_type) or \
             match_mime(application_json, content_type):
             raw_body = input.read()
             charset = content_type.props.get('charset', 'utf8')
             json_src = raw_body.decode(charset)
             try:
                 body = json.loads(json_src)
             except ValueError:
                raise ResourceException(ResourceException.reason_malformed)
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
