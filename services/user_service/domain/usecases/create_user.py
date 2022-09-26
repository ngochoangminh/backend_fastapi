
from typing import Tuple, Any
from core.types.failure import Failure
from .base import BaseUserUsecase

class CreateUserUsecase(BaseUserUsecase):
    async def execute(self, *args, **kwargs) -> Tuple[Any, Failure]:
        return await self.repository.create_user(*args, **kwargs)