
import typing
import json
from loguru import logger
from typing import Any, Optional, TypeVar
from uuid import UUID
import asyncpg
from pydantic import BaseModel
from starlette.background import BackgroundTask
from fastapi.responses import JSONResponse

from datetime import datetime
from core.utils.datetime_utils import format_utc_str


DataType = TypeVar("DataType")

def to_camel(string: str) -> str:
    string_split = string.split('_')
    return string_split[0]+''.join(word.capitalize() for word in string_split[1:])


json_encoders = {
    datetime: format_utc_str,
    UUID: lambda x: str(x),
    asyncpg.pgproto.pgproto.UUID: lambda x: str(x)
}

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

class BaseResponseModel(BaseModel):
    status: int = 200
    message: str = 'success'
    data: Any | None | dict | Optional[DataType] = None

    class Config:
        json_encoders = json_encoders
        alias_generator = to_camel

BaseResponseSchema = BaseResponseModel

class BaseResponse(JSONResponse):
    def __init__(
        self, 
        content: Any,
        status_code: int = 200,
        headers: typing.Optional[dict] = None, 
        media_type: typing.Optional[str] = None,
        background: typing.Optional[BackgroundTask] = None) -> None:
        if isinstance(content, BaseResponseModel):
            status_code = content.status
            content = content.dict(exclude_none=True, by_alias=True)
        elif isinstance(content, dict) or isinstance(content, list):
            content = _cast_data_types(content)
            
            
        # print('content', content)
        # print('content', type(content))

        super().__init__(content, status_code, headers, media_type, background)
    
        