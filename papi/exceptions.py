class RestException(Exception):
    def get_http_status(self):
        return (400, 'Bad Request')

class MalformedException(RestException):
    def get_http_status(self):
        return (400, 'Malformed Input')

class NotFoundException(RestException):
    def get_http_status(self):
        return (404, 'Not Found')

class MethodNotAllowedException(RestException):
    def get_http_status(self):
        return (405, 'Method Not Allowed')

class NotAcceptableException(RestException):
    def get_http_status(self):
        return (406, 'Not Acceptable')

class ConflictException(RestException):
    def get_http_status(self):
        return (409, 'Conflict')

class UnsupportedMediaException(RestException):
    def get_http_status(self):
        return (415, 'Unsupported Media Type')
