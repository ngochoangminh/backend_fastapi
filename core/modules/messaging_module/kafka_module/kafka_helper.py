import  asyncio
import traceback
import confluent_kafka
import itertools
import nanoid
from kink import inject
from typing import List
from loguru import logger
from functools import partial
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException, OFFSET_BEGINNING, OFFSET_END
from core.modules.redis_module.redis_helper import RedisHelper
from ....configs.kafka_settings import KafkaSettings
from ..messaging_interface import MessagingInterface

@inject
class KafkaHelper(MessagingInterface):
    def __init__(self, cfg: KafkaSettings, rdb: RedisHelper, loop=None) -> None:
        
        self.configs=cfg
        self._loop=loop or asyncio.get_event_loop()
        self._rdb=rdb
        self.channel_handeler_map=dict()
        self.channel_broadcast_handeler_map=dict()
        self.flag_close=False
        self.current_offsets=dict()
        self.current_broadcast_offsets=dict()
        self.existing_topics=list()
        self.redis_offset_key=f"__curent-kafka-offset-{self.configs.KAFKA_GROUP_ID}__"
        self.redis_broadcast_offset_key="__curent-kafka-offset-BROADCAST__"
    