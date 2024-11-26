from exception.ApiCodeEnum import ApiCodeEnum


class ApiException(RuntimeError):

    def __init__(self, code: ApiCodeEnum, message):
        self.code = code.value
        self.message = message
