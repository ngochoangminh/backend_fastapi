import uuid

from pydantic import BaseModel, EmailStr

from user_case.pydantic import PhoneStr


class BaseApplication(BaseModel):

    phone: PhoneStr
    email: EmailStr
    text: str
