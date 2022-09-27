from core.configs import CoreSettings, SqlDatabaseSettings, CacheDBSettings, GrpcServerSettings
from kink import di
from dotenv import load_dotenv
load_dotenv('./services/user_service/.env')

"""
Settings for User Management Service
"""
class Settings(CoreSettings, SqlDatabaseSettings, CacheDBSettings, GrpcServerSettings):
    HOST: str
    PORT: str
    USER_API_PREFIX: str = ''
    

    class Config(object):
        case_sensitive = True


cfg = Settings()

di['cfg'] = cfg
di[Settings] = cfg
di[CoreSettings] = cfg
di[SqlDatabaseSettings] = cfg
di[CacheDBSettings] = cfg
di[GrpcServerSettings] = cfg