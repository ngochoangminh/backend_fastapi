from kink import di

from .config.setting import cfg
from core.modules.redis_module import RedisHelper

from .domain.repository import UserRepository
from .data.repository_impl import UserRepositoryImpl
from core.modules.grpc_module.grpc_module import GrpcModule

async def init_di():
    di[UserRepository] = UserRepositoryImpl()
    di[RedisHelper] = RedisHelper(cfg)
    di[GrpcModule] = GrpcModule()