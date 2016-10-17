import logging
import json
from papi.serve import serve_resource
import papi.fp as fp
from papi.mime import match_mime, parse_mime_type

logger = logging.getLogger(__name__)

class DictResource(object):
    def __init__(self, data=None, children=None):
        self.data = data or {}
        self.children = None if children is None else dict(children)

    def get_structured_body(self, **kwargs):
        return self.data

    def get_typed_body(self, mime_pattern):
        if isinstance(self.data, str):
            text_plain_utf8 = parse_mime_type("text/plain;charset=utf8")
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

def application(env, start_response):
    logger.info(env)

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
    return serve_resource(root, env, start_response)
