from pydantic import BaseModel
from bson import ObjectId
from uuid import UUID
from datetime import  datetime


from core.utils.datetime_utils import format_utc_str

def to_camel(string: str) -> str:
    string_split = string.split('_')
    return string_split[0]+''.join(word.capitalize() for word in string_split[1:])


class BasePydantic(BaseModel):

    class Config:
        ignore_extra = True
        json_decoders = {
            ObjectId: str, 
            UUID: str,
            datetime : format_utc_str
            
            }
        allow_population_by_field_name = True
        alias_generator = to_camel