# RestException hierarchy
#
# RestExceptions signal errors at the REST level, which maps directly to HTTP
# and can thus be expressed in terms of an HTTP status code and a reason string.

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

# ResourceException hierarchy
#
# ResourceExceptions describe failures at the "storage" level, i.e., reasons
# why a get, store, or delete operation failed.

class ResourceException(Exception):
    reason_wrong_type = 'type'
    reason_malformed = 'malformed'
    reason_exists = 'exists'
    reason_does_not_exist = 'not_exists'

    rest_exception_mapping = {
        reason_wrong_type: UnsupportedMediaException,
        reason_malformed: MalformedException,
        reason_exists: ConflictException,
        reason_does_not_exist: NotFoundException
    }

    def __init__(self, reason):
        Exception.__init__(self, reason)
        self.reason = reason

    def raise_as_rest_exception(self):
        ctor = self.rest_exception_mapping.get(self.reason, RestException)
        raise ctor()
