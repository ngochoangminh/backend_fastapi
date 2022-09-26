
from dataclasses import dataclass
from core.base import CommonEntity
from ..entities import user

@dataclass
class User(CommonEntity):
    first_name: str
    last_name: str
    username: str
    phone: str
    email: str
    role: str
    password: str