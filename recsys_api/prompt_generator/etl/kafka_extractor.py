import logging
from typing import Generator

import backoff
from core.config import config
from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KafkaExtractor:
    def __init__(self, kafka_consumer: KafkaConsumer):
        self.consumer = kafka_consumer

    def extract(self) -> Generator[ConsumerRecord, None, None]:
        try:
            yield from self.consumer
        except Exception as error:
            logger.error(f"Error: {error}")

    def commit(self):
        self.consumer.commit()


@backoff.on_exception(backoff.expo, Exception, max_tries=config.BACKOFF_MAX_TRIES)
def get_kafka_extractor():
    consumer = KafkaConsumer(
        config.KAFKA_TOPIC_RECSYS,
        bootstrap_servers=[config.KAFKA_DSN],
        auto_offset_reset='earliest',
        group_id='echo-messages-to-stdout',
        enable_auto_commit=False,
    )
    return KafkaExtractor(consumer)
