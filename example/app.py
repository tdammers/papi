import logging
import json
from papi.serve import serve_resource

logger = logging.getLogger(__name__)

class MyResource(object):
    def list(self, *args, **kwargs):
        return [1, 2, 3]

def application(env, start_response):
    logger.info(env)

    return serve_resource(MyResource(), env, start_response)

    # headers = [
    #     ('Content-type', 'text/plain;charset=utf8')
    # ]
    # body = ''
    # for k,v in sorted(dict(env).items()):
    #     try:
    #         v = json.dumps(v)
    #     except TypeError:
    #         v = repr(v)
    #     body += "{0}: {1}\n".format(k, v)

    # start_response('200 OK', headers)
    # return body.encode('utf8')
