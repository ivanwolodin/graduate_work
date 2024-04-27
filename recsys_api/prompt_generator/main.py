import datetime
import json
import logging
import time

from core.config import config

from etl.data_transform import get_transformer
from etl.kafka_extractor import get_kafka_extractor
from etl.kafka_producer import get_kafka_producer

extractor_kafka = get_kafka_extractor()
kafka_producer = get_kafka_producer()

transformer = get_transformer()

logging.basicConfig()
logger = logging.getLogger(__name__)


def main():
    logger.info("Prompt generating started")
    messages = []
    while True:
        try:
            data = extractor_kafka.extract()
            for transformed_data in transformer.transform(data):
                messages.append(transformed_data)
                if len(messages) >= config.ETL_BATCH_MESSAGE_COUNT:
                    kafka_producer.produce(
                        topic=config.KAFKA_TOPIC_RECSYS_PROMPT,
                        key=datetime.datetime.now().strftime(f'%Y-%m-%d:%H:%M:%S'),
                        data=json.dumps(messages),
                    )

                    messages = []
                    extractor_kafka.commit()
        except Exception as e:
            logger.error(f"Error: {e}")
        time.sleep(config.ETL_SLEEP_SECOND)
        continue


if __name__ == "__main__":
    main()
