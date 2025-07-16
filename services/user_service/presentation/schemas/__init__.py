from pydantic import BaseModel 
from core.statics.error_codes import ErrorCodesScheme


class BadRequestResponseModel(BaseModel):
    status: int = 400
    message: str = "Bad Request"
    error_code: str = ErrorCodesScheme.BAD_REQUEST.value
    data: None

    class Config:
        use_enum_values = True


class UnauthorizedRequestResponseModel(BaseModel):
    status: int = 401
    message: str = "Unauthorized Request"
    error_code: str = ErrorCodesScheme.UNAUTHORIZE.value
    data: None

    class Config:
        use_enum_values = True


class ForbiddenResponseModel(BaseModel):
    status: int = 403
    message: str = "Forbidden"
    error_code: str = ErrorCodesScheme.BaseModel.value
    data: None

    class Config:
        use_enum_values = True


class HTTPExceptionResponseModel(BaseModel):
    detail: str = "Forbidden"


class NotFoundResponseModel(BaseModel):
    status: int = 404
    message: str = "Not Found"
    error_code: str = ErrorCodesScheme.NOT_FOUND.value
    data: None = None
    status_code: int = 404

    class Config:
        use_enum_values = True


class Unprocessable(BaseModel):
    status: int = 422
    message: str = "Unprocessable Content"
    error_code: str = ErrorCodesScheme.UNPROCESSABLE.value
    data: None

    class Config:
        use_enum_values = True


class InternalServerErrorModel(BaseSchema):
    status: int = 500
    message: str = "Internal Server Error"
    error_code: str = ErrorCodesScheme.INTERNAL_SERVER_ERROR.value
    data: None

    class Config:
        use_enum_values = True