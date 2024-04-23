import datetime
import json
import logging
import time
from random import randrange

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


def get_film_name(films_id: str):
    films = [
        "Star Trek: The Original Series",
        "Star Trek: Bridge Commander",
        "Star Tours: The Adventures Continue",
        "My Love from Another Star",
        "Empire of Dreams: The Story of the 'Star Wars' Trilogy",
        "Fist of the North Star",
        "Fist of the North Star 2",
        "Star Trek Voyager: Elite Force",
        "Star Fox 64 3D",
        "Star Wars Celebration 2017",
    ]
    return films[randrange(10)]


def main():
    logger.info("ETL started")
    messages = []
    while True:
        try:
            data = extractor_kafka.extract()
            for transformed_data in transformer.transform(data):
                messages.append(transformed_data)
                if len(messages) >= config.ETL_BATCH_MESSAGE_COUNT:
                    if loader_clickhouse.load(data=messages, table_name=config.TABLE_NAME):

                        likes_from_db = loader_clickhouse.create_recsys_task(data=messages,
                                                                             table_name=config.TABLE_NAME)
                        likes = []
                        for like in likes_from_db:
                            for user_id, like_list in like.items():
                                likes.append({user_id: [get_film_name(like) for like in like_list]})

                        kafka_producer.produce(
                            topic=config.KAFKA_TOPIC_RECSYS,
                            key=datetime.datetime.now().strftime('%Y-%m-%d:%H:%M:%S'),
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
