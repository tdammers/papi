def parse_request(environ):
    request = dict()
    request['path'] = parse_path(environ['PATH_INFO'])
    request['accept'] = environ['HTTP_ACCEPT'].split(',')
    request['headers'] = get_headers(environ)
    request['method'] = environ['REQUEST_METHOD']
    request['query'] = parse_query_string(environ['QUERY_STRING'])
    return request

def get_headers(environ):
    headers = []
    for name, val in dict(environ).items():
        if name.startswith('HTTP_'):
            headers.append((name[5:], val))
            
def parse_query_string(s):
    parts = s.split('&')
    return parts

def parse_path(s, skip_trailing_slash=True):
    parts = s.split('/')
    if parts == []:
        return parts
    if parts[0] == '':
        parts = parts[1:]
    if skip_trailing_slash and parts[-1] == '':
        parts = parts[:-1]
    return parts
