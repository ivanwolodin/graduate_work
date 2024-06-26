from backoff import backoff
from constants import ES_INDEX_NAME, ES_INDEX_STRUCTURE
from es_connection import open_elasticsearch_connection
from logger import logger


@backoff()
def create_es_index():
    with open_elasticsearch_connection() as es:
        if not es.indices.exists(index=ES_INDEX_NAME):
            es.indices.create(index=ES_INDEX_NAME, body=ES_INDEX_STRUCTURE)
            logger.info('index was created!')
        else:
            logger.info('index already created!')
