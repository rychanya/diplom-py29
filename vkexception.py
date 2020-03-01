class VKBaseException(Exception):
    pass


class VKPermissionException(VKBaseException):
    pass


class VKTooManyRequestsException(VKBaseException):
    pass


class VKOtherException(VKBaseException):
    pass


def check_response_and_raise(data):
    if 'error' in data:
        error_code = data['error'].get('error_code')
        error_msg = data['error'].get('error_msg')
        if error_code in (15, 7, 18, 30, 260):
            raise VKPermissionException(error_code, error_msg)
        elif error_code == 6:
            raise VKTooManyRequestsException(error_code, error_msg)
        else:
            raise VKOtherException(error_code, error_msg)
    elif 'response' in data:
        return
    else:
        raise VKOtherException(data)
