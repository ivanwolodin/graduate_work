import os

from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    PROJECT_NAME: str = Field("ugc", env="PROJECT_NAME")
    UGC_TOPIC_NAME: str = Field("ugc", env="UGC_TOPIC_NAME")
    KAFKA_HOST: str = Field("kafka", env="KAFKA_HOST")
    KAFKA_PORT: str = Field("29099", env="KAFKA_PORT")


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    pass


def get_config() -> Config:
    mode = os.getenv('PRODUCTION_MODE', 'false')
    if mode.lower() == 'true':
        return ProductionConfig()
    return DevelopmentConfig()


config = get_config()
