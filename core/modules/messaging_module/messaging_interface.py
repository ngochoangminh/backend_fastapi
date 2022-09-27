from abc import abstractmethod
from typing import List

class MessagingInterface:

    @abstractmethod
    def __init__(self, configs, rdb=None) -> None: raise NotImplementedError

    @abstractmethod 
    async def create_topics(self, topics:List[str],num_partitions=1, replication_factor=1, topic_configs=None) -> dict: raise NotImplementedError

    @abstractmethod
    async def send(self, topic, data, on_delivery) -> None: raise NotImplementedError

    @abstractmethod
    async def send_json(self, topic, json_data, on_delivery) -> None: raise NotImplementedError

    @abstractmethod
    async def subscribe(self, topics, callback, is_json, is_broadcast) -> None: raise NotImplementedError

    @abstractmethod
    async def unsubscribe(self, topic, key) -> None: raise NotImplementedError

    @abstractmethod
    async def flush(self) -> None: raise NotImplementedError

    @abstractmethod
    async def close(self) -> None: raise NotImplementedError

    @abstractmethod
    async def delete_topics(self, topics: List[str], *args, **kwargs): raise NotImplementedError