from pydantic import BaseModel, EmailStr
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class UserBased(BaseModel):
    first_name: str
    last_name: str
    birth_date: str
    gender: str
    email: str
    phone_number: str
    address: str
    is_admin: bool