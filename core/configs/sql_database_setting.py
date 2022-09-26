from loguru import logger
from typing import Any, Dict
from pydantic import BaseSettings, PostgresDsn, validator

class SqlDatabaseSettings(BaseSettings):

    DB_HOST: str = ''
    DB_PORT: str = ''
    DB_PASSWORD: str = ''
    DB_USER: str = ''
    DB_NAME: str = ''
    DATABASE_URI: str = None

    @validator('DATABASE_URI', pre=True)
    def assemble_db_connection(
        cls, value: str, values: Dict[str, Any]
    ) -> str:
        logger.info(f"VALUES {values}")
        if isinstance(values, str) and not value== '' and value is not None:
            return  value
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
             user=values.get('DB_USER'),
            password=values.get('DB_PASSWORD'),
            host=values.get('DB_HOST'),
            port=values.get('DB_PORT'),
            path='/{0}'.format(values.get('DB_NAME')),
        )
    
    class config(object):
        case_sensitive = True