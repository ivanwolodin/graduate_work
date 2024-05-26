import datetime
import json
import logging
import time
from random import randrange

from core.config import config

# from etl.clickhouse_loader import get_clickhouse_loader
from etl.data_transform import get_transformer
from etl.kafka_extractor import get_kafka_extractor
from etl.kafka_producer import get_kafka_producer
from giga import get_suggestion

extractor_kafka = get_kafka_extractor()
kafka_producer = get_kafka_producer()

transformer = get_transformer()

# loader_clickhouse = get_clickhouse_loader()
# loader_clickhouse.create_structure(config.TABLE_NAME)

logging.basicConfig()
logger = logging.getLogger(__name__)


def get_film_name(films_id: str):
    films = [
        "Винни пух",
        "Звездные войны",
        "Смешарики",
        "Ну погоди",
        "Фиксики",
    ]
    return films[randrange(5)]


def main():
    logger.info("ETL started")
    messages = []
    while True:
        try:
            qui_i = 0
            data = extractor_kafka.extract()
            for transformed_data in transformer.transform(data):
                # messages.append(transformed_data)
                suggestions = []
                for user_likes in transformed_data:
                    for user_id, like_prompt in user_likes.items():
                        suggestions = get_suggestion(
                            like_prompt,
                            ' пользователю больше 18 лет',
                            ', нужны фильмы на новогоднюю тематику, наименования фильмов выводи на английском языке ')
                    logger.info(suggestions)
                messages.append(suggestions)
                logger.info(messages)
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
