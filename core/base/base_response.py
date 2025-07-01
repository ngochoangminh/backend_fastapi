import datetime
import typing
from uuid import UUID
from fastapi import BackgroundTasks, Query
from loguru import logger
from pydantic import BaseModel
import decimal
# from pydantic.datetime_parse import parse_datetime
from fastapi.responses import JSONResponse
from app.common.response.http_code import Failure
from app.common.utils.converters.datetime_converter import DatetimeConverter


def to_camel(string: str) -> str:
    string_split = string.split("_")
    return string_split[0] + "".join(word.capitalize() for word in string_split[1:])


json_encoders = {datetime: DatetimeConverter.format_utc_str, UUID: lambda x: str(x)}

def validate_data(check):
    if isinstance(check, datetime.datetime):
        return check.isoformat()
    elif isinstance (check, datetime.date):
        return check.isoformat()
    elif isinstance(check, decimal.Decimal):
        try:
            return int(check)
        except Exception:
            logger.debug(f"Value of check: {check}")
            return float(check)
    else:
        return check  

def delete_additional_keys(entity: dict, secondary_field: str = None, fk: bool = True):
    if "_sa_instance_state" in entity:
        del entity["_sa_instance_state"]
        
    if "update_data" in entity:
        del entity['update_data']

    entity["uid"] = entity.get("uid") if isinstance(entity.get("uid"), str) else int(entity.get("uid")) 
    if "_id" in entity:
        entity["_id"] = str(entity["_id"])

    for k,v in entity.items():
        entity[k]=validate_data(v)


    if secondary_field:
        entity[secondary_field] = str(entity.get(secondary_field))


def _cast_data_types(data):
    if isinstance(data, dict):
        data = {k: _cast_data_types(v) for k, v in data.items()}
    elif isinstance(data, list):
        data = [_cast_data_types(v) for v in data]
    else:
        _type = type(data)
        if _type in json_encoders:
            return json_encoders[_type](data)
    return data


class StringDate(datetime.datetime):
    @classmethod
    def __get_validators__(cls):
        # yield parse_datetime  #TODO: Adapt to Pydantic V2 with https://docs.pydantic.dev/2.0/usage/serialization/#custom-serializers
        yield cls.validate

    @classmethod
    def validate(cls, v: datetime):
        return DatetimeConverter.format_utc_str(v)


class AllOptional(BaseModel):
    def __new__(self, name, bases, namespaces, **kwargs):
        annotations = namespaces.get("__annotations__", {})
        for base in bases:
            annotations.update(base.__annotations__)
        for field in annotations:
            if not field.startswith("__"):
                annotations[field] = typing.Optional[annotations[field]]
        namespaces["__annotations__"] = annotations
        return super().__new__(self, name, bases, namespaces, **kwargs)


class BaseSchema(BaseModel):
    class Config:
        use_enum_values = True
        from_attributes = True
        ignore_extra = True
        populate_by_name = True
        # alias_generator = to_camel
        json_encoders = json_encoders
        ser_json_inf_nan = 'constants'


class RawParams(BaseModel):
    limit: int
    offset: int


class PaginationParams(BaseModel):
    page: int = Query(1, ge=1, description="Page number")
    size: int = Query(10, ge=1, le=100, description="Page size")

    def to_raw_params(self) -> RawParams:
        return RawParams(limit=self.size, offset=self.size * (self.page - 1))


class PaginationModel(BaseSchema):
    items: typing.List[typing.Any] = []
    size: int
    page: int
    total: int

    class Config:
        use_enum_values = True


class BaseResponseModel(BaseSchema):
    status: int = 200
    message: str = "Success!"
    data: typing.Any | None | dict = None

    class Config:
        use_enum_values = True


class BaseResponse(JSONResponse):
    def __init__(
        self,
        content: typing.Any,
        status_code: int = 200,
        # error_code: str = None,
        headers: typing.Optional[dict] = None,
        cookies: typing.Optional[dict] = None,
        cookie_domain: typing.Optional[str] = None,
        media_type: typing.Optional[str] = None,
        background: typing.Optional[BackgroundTasks] = None,
    ) -> None:
        if isinstance(content, BaseResponseModel):
            status_code = content.status
            content = content.model_dump(
                # exclude_none=True, 
                by_alias=True
            )
        elif isinstance(content, Failure):
            status_code = content.code
            content = {
                "errorCode": content.error_code,
                "detail": content.message,
                "data": [],
            }

        elif isinstance(content, PaginationModel):
            content = content.model_dump(
                # exclude_none=True, 
                by_alias=True
            )

        super().__init__(content, status_code, headers, media_type, background)
        if cookies:
            for k, v in cookies.items():
                self.set_cookie(
                    key=k, value=v, domain=cookie_domain, secure=True, httponly=False
                )


class BaseExceptionResponse(Exception):
    def __init__(self, message: str, code: int = 400) -> None:
        self.message = message
        self.code = code
        super().__init__(self.message)
