# A resource can be any object that implements the following protocol:
#
# PROPERTIES
#
# name
# """ The machine-readable name for the resource. This should be a valid
# URI path element, and by convention, should only use alphanumeric ASCII
# characters and/or - and _. Other characters will probably also work but
# produce ugly URLs.
# """
#
# METHODS
#
# def list(self, offset=0, limit=None, ordering=None):
# """ Returns one of:
# a) a list of documents according to the specified pagination and ordering.
# b) a dictionary containing the keys "count" (specifying the total number of
#    objects in the list; optional) and "items" (the actual items after
#    pagination and ordering).
# """
#
# def item(self, key):
# """ Returns the document for the specified key, or None if the document
# could not be found.
# """
#
# def store(self, item, key=None, overwrite=True):
# """ Creates or updates the item in the collection. If "key" is given, any
# existing item at this position should be overwritten, unless "overwrite" is
# set to False. If "key" is not given, then a new key should be generated by the
# backend.  Returns a tuple of (key, item, action) on successful insertion or
# update (action will be "INSERT" or "UPDATE" to indicate which happened), or
# throws a suitable exception if the insertion failed.
# """
#
# def delete(self, key):
# """ Deletes the item at "key" if it exists. Throws a suitable exception if
# the item cannot be deleted or doesn't exist.
# """
