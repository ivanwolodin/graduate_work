from typing import Optional

from aiokafka import AIOKafkaProducer
from pydantic import BaseModel

from .base_broker import BaseProducer


class KafkaProducer(BaseProducer):

    def __init__(self, producer: AIOKafkaProducer) -> None:
        self.producer = producer

    async def produce(self, topic: str, key: str, data: BaseModel):
        await self.producer.send(
            topic=topic,
            value=data.json().encode('utf-8'),
            key=key.encode('utf-8'),
        )


kafka_producer: Optional[KafkaProducer] = None


def get_kafka_producer():
    return kafka_producer
