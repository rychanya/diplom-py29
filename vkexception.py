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
