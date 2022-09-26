
from abc import abstractmethod
from typing import Tuple
from  core.base import BaseRepository
from core.types.failure import Failure
from ..entities import User

class UserRepository(BaseRepository):

    @abstractmethod
    async def create_user(self, data: dict, *args, **kwargs) -> Tuple[User, Failure]: raise NotImplementedError
