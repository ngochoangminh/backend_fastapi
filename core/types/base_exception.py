from app.common.statics.error_codes import ErrorCodesScheme


class BaseException(Exception):
    status_code: int

    def __init__(
            self,
            message: str = "Bad Request",
            error_code: str = ErrorCodesScheme.UNKNOWN.value,
            status_code: int = 400,
    ):
        self.message = message
        self.error_code = error_code
        # if not getattr(self, 'status_code'):
        self.status_code = status_code

    @property
    def code(self):
        return self.status_code


class UnauthorizedException(BaseException):
    status_code = 401

    def __init__(self, message: str = "Unauthorized!"):
        error_code = ErrorCodesScheme.UNAUTHORIZE.value
        super().__init__(message, error_code, self.status_code)


class ForbiddenException(BaseException):
    status_code = 403

    def __init__(self, message: str = "Forbidden!"):
        error_code = ErrorCodesScheme.FORBIDDEN.value
        super().__init__(message, error_code, self.status_code)


class NotFoundException(BaseException):
    status_code = 404

    def __init__(self, message: str = "Not Found!"):
        error_code = ErrorCodesScheme.NOT_FOUND.value
        super().__init__(message, error_code, self.status_code)


class InvalidInputException(BaseException):
    status_code = 422

    def __init__(self, message: str = "Invalid input!"):
        error_code = ErrorCodesScheme.INVALID_INPUT.value
        super().__init__(message, error_code)

class DataErrorException(BaseException):
    status_code = 404

    def __init__(self, message: str = "Data Error!"):
        error_code = ErrorCodesScheme.DATA_ERROR.value
        super().__init__(message, error_code, self.status_code)

class InternalServerErrorException(BaseException):
    status_code = 500

    def __init__(self, message: str = "Internal Server Error!"):
        error_code = ErrorCodesScheme.DATA_ERROR.value
        super().__init__(message, error_code, self.status_code) 

class ConflictException(BaseException):
    status_code = 409

    def __init__(self, message: str = "Conflict!"):
        error_code = ErrorCodesScheme.CONFLICT.value
        super().__init__(message, error_code, self.status_code)             
            
class FMCInvalidDataError(BaseException):
    pass