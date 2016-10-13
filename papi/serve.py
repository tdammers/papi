import logging
from papi.request import parse_request
from papi.exceptions import RestException, \
                            MalformedException, \
                            NotFoundException, \
                            MethodNotAllowedException, \
                            NotAcceptableException, \
                            ConflictException, \
                            UnsupportedMediaException
from traceback import format_exc
import json

logger = logging.getLogger(__name__)

def serve_resources(resources, environ, start_response):
    request = parse_request(environ)
    status, headers, body = handle_resources(resources, request)
    status_str = "{0} {1}".format(*status)
    start_response(status_str, headers)
    if type(body) is str:
        body = body.encode('utf8')
    return body

def handle_resources(resources, request):
    if request['path'] == []:
        return handle_resource_list(resources, request)
    else:
        new_request = dict(request)
        new_request['path'] = request['path'][1:]
        key = request['path'][0]
        resource = resources.get(key)
        if resource is None:
            raise NotFoundException()
        return handle_resource(resource, new_request)

def handle_resource_list(resources, request):
    return (
        (200, 'OK'),
        [('Content-type', 'text/json;charset=utf8')
        ],
        json.dumps(list(sorted(resources.keys()))))


def handle_resource(resource, request):
    try:
        if request['path'] == []:
            return handle_collection(resource, request)
        elif len(request['path']) == 1:
            key = request['path'][0]
            return handle_item(key, resource, request)
        else:
            raise NotFoundException()
    except RestException as e:
        status_code, status_message = e.get_http_status()
        try:
            body = e.args[0]
        except IndexError:
            body = status_message
        return (
            (status_code, status_message),
            [('Content-type', 'text/plain;charset=utf8')
            ],
            body.encode('utf-8')
        )
    except Exception:
        status_code, status_message = 500, 'Internal Server Error'
        body = "Something went wrong"
        logger.error(format_exc())
        return (
            (status_code, status_message),
            [('Content-type', 'text/plain;charset=utf8')
            ],
            body.encode('utf-8')
        )

def handle_collection(resource, request):
    handler = collection_handlers.get(request['method'])
    if handler is None:
        raise MethodNotAllowedException()
    return handler(resource, request)

def handle_item(key, resource, request):
    handler = item_handlers.get(request['method'])
    if handler is None:
        raise MethodNotAllowedException()
    return handler(key, resource, request)

def collection_GET(resource, request):
    if 'list' in dir(resource):
        items = resource.list()
    else:
        raise MethodNotAllowedException()
    if items is None:
        items = []
    try:
        reply = {
            'count': items['count'],
            'items': items['items']
        }
    except TypeError:
        reply = {
            'count': len(items),
            'items': items
        }

    return (
        (200, 'OK'),
        [('Content-type', 'application/json')
        ],
        json.dumps(reply)
    )

def item_GET(key, resource, request):
    if 'item' in dir(resource):
        item = resource.item(key)
    else:
        raise MethodNotAllowedException()
    if item is None:
        raise NotFoundException()
    return (
        (200, 'OK'),
        [('Content-type', 'application/json')
        ],
        json.dumps(item)
    )

collection_handlers = {
    'GET': collection_GET
}

item_handlers = {
    'GET': item_GET
}
