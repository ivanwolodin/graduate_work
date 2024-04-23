import backoff
from clickhouse_driver import Client
from core.config import \
    config  # BACKOFF_MAX_TRIES, CLICK_HOST, CLICK_PORT, DB_NAME
from models.content_model import BaseContent


class ClickHouseLoader:
    def __init__(self, client: Client):
        self.client = client

    @backoff.on_exception(backoff.expo, Exception, max_tries=config.BACKOFF_MAX_TRIES)
    def create_structure(self, table_name: str) -> None:
        self.client.execute(f"CREATE DATABASE IF NOT EXISTS {config.DB_NAME} ON CLUSTER company_cluster")
        self.client.execute(
            f"""CREATE TABLE IF NOT EXISTS {config.DB_NAME}.{table_name} ON CLUSTER company_cluster \
            (user_id VARCHAR, content_type VARCHAR, object_id VARCHAR, metrics INTEGER, update_date DateTime DEFAULT now()) ENGINE = MergeTree() \
            ORDER BY (user_id, content_type)"""
        )

    @backoff.on_exception(backoff.expo, Exception, max_tries=config.BACKOFF_MAX_TRIES)
    def load(self, table_name: str, data: list[BaseContent]) -> int | None:
        query = f"""INSERT INTO {config.DB_NAME}.{table_name} (user_id, content_type, object_id, metrics) VALUES"""
        query_params = ((row.user_id, row.content_type, row.object_id, row.metrics) for row in data)
        return self.client.execute(query, query_params)

    @backoff.on_exception(backoff.expo, Exception, max_tries=config.BACKOFF_MAX_TRIES)
    def create_recsys_task(self, table_name: str, data: list[BaseContent]) -> list:
        likes = []
        for row in data:
            query = f"""
                select user_id, content_type, object_id, metrics
                from {config.DB_NAME}.{table_name}
                where user_id='{row.user_id}' and content_type='0'"""
            likes.append({row.user_id: self.client.execute(query)})
        return likes


@backoff.on_exception(backoff.expo, Exception, max_tries=config.BACKOFF_MAX_TRIES)
def get_clickhouse_loader():
    client = Client(host=config.CLICK_HOST, port=config.CLICK_PORT)
    return ClickHouseLoader(client)
