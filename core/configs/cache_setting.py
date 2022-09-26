import os
from pydantic import BaseSettings

class CacheDBSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: int 
    REDIS_PASSWORD: str
    REDIS_EXPIRE_SECOND: int

    CACHE_CONN_STR: str = f"redis://:{os.environ.get('REDIS_PASSWORD')}@{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}"

    class Config(object):
        case_sensitive = True