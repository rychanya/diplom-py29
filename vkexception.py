class VKBaseException(Exception):
    pass


class VKPermissionDenied(VKBaseException):
    pass


class VKTooManyRequests(VKBaseException):
    pass


class VKUserWasDeletedOrBanned(VKBaseException):
    pass


class VKOtherException(VKBaseException):
    pass

# "{7: 'Permission to perform this action is denied', 6: 'Too many requests per second', 18: 'User was deleted or banned'}"
