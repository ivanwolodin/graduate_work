from functools import lru_cache

from broker.base_broker import BaseProducer
from broker.kafka_broker import KafkaProducer, get_kafka_producer
from core.config import config
from fastapi import Depends
from models.content_model import BaseContent


class ContentService:

    def __init__(self, producer: BaseProducer):

        self.producer: BaseProducer = producer
        self.topic: str = config.UGC_TOPIC_NAME

    async def produce(self, data: BaseContent) -> None:
        await self.producer.produce(topic=self.topic, key=f'{data.user_id}:{data.content_type}', data=data)


@lru_cache()
def get_content_loader_service(producer: KafkaProducer = Depends(get_kafka_producer)) -> ContentService:
    return ContentService(producer)
