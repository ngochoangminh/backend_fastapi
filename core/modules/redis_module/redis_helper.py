
import json
import time
import traceback
from loguru import logger
import aioredis
from kink import inject

from core.configs import CacheDBSettings

class RedisLockError(Exception):
    def __init__(self, message):
        self.message = message

@inject
class RedisHelper:

    def __init__(self, cfg: CacheDBSettings) -> None:
        
        self.host = cfg.REDIS_HOST
        self.port = cfg.REDIS_PORT
        self.db = cfg.REDIS_DB
        password = cfg.REDIS_PASSWORD
        self.exp_seccond =  cfg.REDIS_EXPIRE_SECOND
        # self.error_callback = error_callback
        self.error_count = 0

        logger.info(f'Connecting to redis at host {self.host} port {self.port}')
        self.pool_count = 1
        try:
            self.io_rdbs = [aioredis.Redis(host=self.host,
                                           port=self.port, db=self.db, password=password) for i in range(self.pool_count)]
            # Specialized for management jobs
            self.mng_rdb = aioredis.Redis(host=self.host,
                                          port=self.port, db=self.db, password=password)
        except:
            logger.error(f'error connect redis {traceback.format_exc()}')
            # self.error_callback(-1)
        self.lock_ids = {}  # lockid to resource name

        self.key_to_rdb = {}  # key to indx of rdb
        self.next_rdb_idx = 0  # round robin
        self.last_used_time = {} # key -> last timestamp
        self.last_clean_time = time.time()
        self.clean_time_thresh = 15*60

    def _rdb(self, is_manager, key) -> aioredis.Redis:
        if is_manager:
            return self.mng_rdb
        else:
            if not key in self.key_to_rdb:
                self.key_to_rdb[key] = self.next_rdb_idx

                self.next_rdb_idx += 1
                if self.next_rdb_idx >= len(self.io_rdbs):
                    self.next_rdb_idx = 0
            
            rdb_idx = self.key_to_rdb[key]
            now = time.time()
            self.last_used_time[key] = now

            if now - self.last_clean_time > self.clean_time_thresh:
                cleaned_keys = []

                for k, timestamp in self.last_used_time.items():
                    if now - timestamp > self.clean_time_thresh:
                        cleaned_keys.append(k)
                for k in cleaned_keys:
                    self.key_to_rdb.pop(k)
                    self.last_used_time.pop(k)

            return self.io_rdbs[rdb_idx]

    async def set(self, key, value, expire_s=None, is_manager=False):
        data = json.dumps(value)
        ex = expire_s if expire_s is not None else self.exp_seccond
        await self._rdb(is_manager, key).set(key, data, ex=ex)

    async def get(self, key, default=None, is_manager=False):
        try:
            result = await self._rdb(is_manager, key).get(key)
            if not result is None:
                result = json.loads(result)
            else:
                result = default

            return result
        except:
            self.error_count += 1
            logger.error(f'error get redis message: {traceback.format_exc()}')
            # if self.error_callback:
            #     self.error_callback(self.error_count)
    
    async def delete(self, key, is_manager=False):
        await self._rdb(is_manager, key).delete(key)