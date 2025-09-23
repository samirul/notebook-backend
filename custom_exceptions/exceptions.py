from rest_framework.exceptions import APIException

class NoUserIsFoundException(Exception):
    pass

class UndefinedException(APIException):
    status_code = 400
    default_detail = "Something went wrong."
    default_code = "undefined_error"

class NoPDFException(APIException):
    status_code = 400
    default_detail = "Something went wrong."
    default_code = "undefined_error"

class NoTEXTException(APIException):
    status_code = 400
    default_detail = "Something went wrong."
    default_code = "undefined_error"


class NotFoundRequiredTypeFileUploadException(APIException):
    status_code = 400
    default_detail = "Something went wrong."
    default_code = "undefined_error"