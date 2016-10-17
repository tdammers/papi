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
import papi.fp as fp
from functools import partial
from papi.hateoas import hateoas

logger = logging.getLogger(__name__)

def serve_resource(resource, environ, start_response):
    request = parse_request(environ)
    request = fp.assocs(
                [
                    ('consumed_path', ()),
                    ('remaining_path', request['path'])
                ],
                request)
    status, headers, body = handle_resource(resource, request)
    status_str = "{0} {1}".format(*status)
    start_response(status_str, headers)
    if type(body) is str:
        body = body.encode('utf8')
    return body

def handle_resource(resource, request):
    remaining_path = fp.prop('remaining_path', request)
    print(remaining_path)
    if len(remaining_path) == 0:
        return handle_resource_self(resource, request)
    else:
        child_name, new_request = consume_path_item(request)
        child = resource.get_child(child_name)
        if child is None:
            raise NotFoundException
        return handle_resource(child, new_request)

def handle_resource_self(resource, request):
    method = fp.prop('method', request).upper()
    logger.warn(method)
    if method == 'GET':
        return handle_resource_get(resource, request)
    # elif method == 'POST':
    #     handle_resource_post(resource, request)
    # elif method == 'PUT':
    #     handle_resource_put(resource, request)
    # elif method == 'DELETE':
    #     handle_resource_delete(resource, request)
    else:
        raise MethodNotAllowedException

def handle_resource_get(resource, request):
    return handle_resource_get_json(resource, request)

def get_resource_digest(resource):
    try:
        digest = resource.get_structured_body(digest=True)
    except AttributeError:
        digest = resource
    return digest

def get_resource_body(resource):
    try:
        digest = resource.get_structured_body()
    except AttributeError:
        digest = resource
    return digest

def handle_resource_get_json(resource, request):
    raw_body = resource.get_structured_body()
    current_path = fp.prop('consumed_path', request)
    name = fp.last(current_path)
    
    offset = fp.path(('query', 'offset'), request)
    count = fp.path(('query', 'count'), request)

    body = hateoas(current_path, raw_body)

    children = resource.get_children(offset=offset, count=count)
    if children is not None:
        children_alist = [
            (k, get_resource_digest(v)) for k, v in children
        ]

        def prepare_child(kv):
            name, value = kv
            if not isinstance(value, dict):
                value = {'_value': value}
            return fp.chain(
                    partial(fp.assoc, '_name', name),
                    partial(hateoas, fp.snoc(name, current_path))
                )(value)

        children_list = list(map(prepare_child, children_alist))
        body['_items'] = children_list
    if name is not None:
        body['_name'] = name
    return make_json_response(body)

def consume_path_item(request):
    first_item = fp.head(fp.prop('remaining_path', request))
    if first_item is None:
        return None, request
    new_request = fp.chain(
        partial(
            fp.Lens.over,
            fp.prop_lens('remaining_path'),
            partial(fp.drop, 1)),
        partial(
            fp.Lens.over,
            fp.prop_lens('consumed_path'),
            partial(fp.snoc, first_item)))(request)
    return first_item, new_request

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
