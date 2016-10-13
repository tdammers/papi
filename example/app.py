import logging
import json
from papi.serve import serve_resources

logger = logging.getLogger(__name__)

class MyResource(object):
    def __init__(self, records):
        self.records = records

    def list(self, *args, **kwargs):
        return self.records

    def item(self, key):
        return self.records.get(key)

    def structure_item(self, item):
        return {
            'message': item
        }

def application(env, start_response):
    logger.info(env)

    things = {
        'apple': "I am an apple. Eat me.",
        'onion': "Hurt me, and I will make you cry.",
        'banana': "I'll bend either way for you.",
        'nut': "I'm nuts!"
    }
    resources = {
        'things': MyResource(things)
    }
    return serve_resources(resources, env, start_response)
