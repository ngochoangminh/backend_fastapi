from core.base import BaseDao
from ..orm import UserORM

class UserDAO(BaseDao):
    model = UserORM

