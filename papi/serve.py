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
    request['parent_path'] = []
    status, headers, body = handle_resources(resources, request)
    status_str = "{0} {1}".format(*status)
    start_response(status_str, headers)
    if type(body) is str:
        body = body.encode('utf8')
    return body

def consume_path(request):
    new_request = dict(request)
    new_request['path'] = request['path'][1:]
    current = request['path'][0]
    new_request['parent_path'].append(current)
    return current, new_request

def handle_resources(resources, request):
    if request['path'] == []:
        return handle_resource_list(resources, request)
    else:
        key, new_request = consume_path(request)
        resource = resources.get(key)
        if resource is None:
            raise NotFoundException()
        return handle_resource(resource, new_request)

def handle_resource_list(resources, request):
    parent_path = request['parent_path']
    items = decorate_list(resources.keys(), parent_path, lambda k: k)
    return make_json_response(items)

def handle_resource(resource, request):
    try:
        if request['path'] == []:
            return handle_collection(resource, request)
        elif len(request['path']) == 1:
            key, new_request = consume_path(request)
            return handle_item(key, resource, new_request)
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
        items = {}
    parent_path = request['parent_path']
    if type(items) is dict:
        items = decorate_dict(items, parent_path)
    else:
        items = decorate_list(items, parent_path, resource.key_prop)
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
    reply = decorate_item(reply, parent_path[:-1], parent_path[-1])
    return make_json_response(reply)

def item_GET(key, resource, request):
    if 'item' in dir(resource):
        item = resource.item(key)
    else:
        raise MethodNotAllowedException()
    if item is None:
        raise NotFoundException()
    parent_path = request['parent_path'][:-1]
    item = decorate_item(item, parent_path, key)
    return make_json_response(item)

def decorate_item(item, parent_path, name=None, name_fn=None):
    if name is None:
        if name_fn is not None:
            name = name_fn(item)
    if not 'keys' in dir(item):
        item = { 'value': item }
    if item.get('_links') is None:
        item['_links'] = {}
    print(parent_path)
    print(name)
    item['_links']['parent'] = '/' + '/'.join(parent_path)
    if name is not None:
        self_path = list(parent_path)
        self_path.append(name)
        item['_links']['self'] = '/' + '/'.join(self_path)
    return item

def decorate_list(items, parent_path, name_fn=None):
    return [ decorate_item(item, parent_path, name_fn=name_fn) for item in items ]

def decorate_dict(items, parent_path):
    return [ decorate_item(v, parent_path, k) for k, v in items.items() ]

def make_json_response(
        data,
        status=200,
        headers=None):
    content_type='application/json'
    headers = list(headers or [])
    headers.append(('Content-type', content_type))
    body = json.dumps(data)
    if type(body) is str:
        body = body.encode('utf8')
    return ((status, status_names.get(status, 'OK')), headers, body)

status_names = {
    200: 'OK',
    201: 'Created',
    204: 'No Content'
}

collection_handlers = {
    'GET': collection_GET
}

item_handlers = {
    'GET': item_GET
}
