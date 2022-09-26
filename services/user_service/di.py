from kink import di

from .configs.setting import cfg
from core.modules.redis_module import RedisHelper

from .domain.repository import UserRepository
from .data.repository_impl import UserRepositoryImpl

async def init_di():
    di[UserRepository] = UserRepositoryImpl()
    di[RedisHelper] = RedisHelper(cfg)