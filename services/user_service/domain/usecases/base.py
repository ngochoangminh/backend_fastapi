
from kink import inject
from ..repository import UserRepository
from core.modules.redis_module import RedisHelper
from core.base import BaseUseCase

class BaseUserUsecase(BaseUseCase):
    def __init__(self, repository: UserRepository, redis: RedisHelper) -> None:
        self.repository = repository
        self.redis = redis