
from msilib.schema import Class
from core.base import BasePydantic as BaseModel
from core.base import BaseResponseModel

class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    phone: str
    password: str
    role: str|None = 'customer'

class UserInfo(BaseModel):
    id: str
    first_name: str
    last_name: str
    username: str
    email: str
    phone: str
    password: str
    role: str

class UserInfoResponse(BaseResponseModel):
    data: UserInfo|None = None