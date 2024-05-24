from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    BACKOFF_MAX_TRIES: int = Field(100, env="BACKOFF_MAX_TRIES")
    # KAFKA_TOPIC_NAME: str = Field("ugc", env="KAFKA_TOPIC_NAME")
    KAFKA_TOPIC_RECSYS: str = Field("recsys", env="KAFKA_TOPIC_RECSYS")
    KAFKA_TOPIC_RECSYS_PROMPT: str = Field("recsys_prompt", env="KAFKA_TOPIC_RECSYS_PROMPT")
    RECSYS_PROMPT_PREFIX_SCRIPT: str = Field("Пользователю нравятся фильмы",
                                                  env="KAFKA_TOPIC_RECSYS_PREFIX_SCRIPT")
    RECSYS_PROMPT_POSTFIX_SCRIPT: str = Field("предложи 10 фильмов которые ему понравятся",
                                                  env="KAFKA_TOPIC_RECSYS_PREFIX_SCRIPT")

    KAFKA_DSN: str = Field("kafka:29099", env="KAFKA_DSN")
    # CLICK_HOST: str = Field("localhost", env="CLICK_HOST")
    # CLICK_PORT: str = Field("9000", env="CLICK_PORT")
    ETL_SLEEP_SECOND: int = Field(5, env="ETL_SLEEP_SECOND")
    ETL_BATCH_MESSAGE_COUNT: int = Field(1, env="ETL_BATCH_MESSAGE_COUNT")
    # TABLE_NAME: str = Field("table_ugc", env="TABLE_NAME")
    # DB_NAME: str = Field("ugc", env="DB_NAME")


config = Config()
