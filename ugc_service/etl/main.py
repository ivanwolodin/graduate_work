import datetime
import json
import logging
import time

from core.config import config

from etl.clickhouse_loader import get_clickhouse_loader
from etl.data_transform import get_transformer
from etl.kafka_extractor import get_kafka_extractor
from etl.kafka_producer import get_kafka_producer

extractor_kafka = get_kafka_extractor()
kafka_producer = get_kafka_producer()

transformer = get_transformer()

loader_clickhouse = get_clickhouse_loader()
loader_clickhouse.create_structure(config.TABLE_NAME)

logging.basicConfig()
logger = logging.getLogger(__name__)


def main():
    logger.info("ETL started")
    messages = []
    while True:
        try:
            qui_i = 0
            data = extractor_kafka.extract()
            for transformed_data in transformer.transform(data):
                messages.append(transformed_data)
                if len(messages) >= config.ETL_BATCH_MESSAGE_COUNT:
                    if loader_clickhouse.load(data=messages, table_name=config.TABLE_NAME):
                        likes = loader_clickhouse.create_recsys_task(data=messages, table_name=config.TABLE_NAME)

                        kafka_producer.produce(
                            topic=config.KAFKA_TOPIC_RECSYS,
                            key=datetime.datetime.now().strftime(f'%Y-%m-%d:%H:%M:%S'),
                            data=json.dumps(likes),
                        )

                        messages = []
                        extractor_kafka.commit()
        except Exception as e:
            logger.error(f"Error: {e}")
        time.sleep(config.ETL_SLEEP_SECOND)
        continue



if __name__ == "__main__":
    main()
