from core.config import config
from kafka import KafkaProducer


class Producer:

    def __init__(self, producer: KafkaProducer) -> None:
        self.producer = producer

    def produce(self, topic: str, key: str, data: str):
        self.producer.send(
            topic=topic,
            value=data.encode('utf-8'),
            key=key.encode('utf-8'),
        )


kafka_producer = Producer(KafkaProducer(bootstrap_servers=[config.KAFKA_DSN]))


def get_kafka_producer():
    return kafka_producer
