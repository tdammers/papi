from urllib.parse import parse_qs

def parse_request(environ):
    return {
        'path': parse_path(environ['PATH_INFO']),
        'accept': environ['HTTP_ACCEPT'].split(','),
        'headers': get_headers(environ),
        'method': environ['REQUEST_METHOD'],
        'query': parse_qs(environ['QUERY_STRING'], keep_blank_values=True),
    }

def get_headers(environ):
    headers = []
    for name, val in dict(environ).items():
        if name.startswith('HTTP_'):
            headers.append((name[5:], val))
            
def parse_path(s, skip_trailing_slash=True):
    parts = s.split('/')
    if parts == []:
        return tuple(parts)
    if parts[0] == '':
        parts = parts[1:]
    if skip_trailing_slash and parts[-1] == '':
        parts = parts[:-1]
    return tuple(parts)
