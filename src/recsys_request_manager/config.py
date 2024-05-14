import os
import logging
from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from utils.logging import StandardFormatter, ColorFormatter


class LoggingConfig(BaseModel):
    version: int
    disable_existing_loggers: bool = False
    formatters: dict
    handlers: dict
    loggers: dict


class Settings(BaseSettings):
    PROJECT_SLUG: str = "request_manager"

    RABBIT_SERVER: str = os.getenv("KAFKA_SERVER")
    PROMPT_TOPIK:  str = os.getenv("PROMPT_TOPIK")
    GIGACHAT_API: str = os.getenv("GIGACHAT_API")
    LOGGING_CONFIG: LoggingConfig = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            'colorFormatter': {'()': ColorFormatter},
            'standardFormatter': {'()': StandardFormatter},
        },
        "handlers": {
            'consoleHandler': {
                'class': 'logging.StreamHandler',
                'level': "DEBUG",
                'formatter': 'standardFormatter',
                'stream': 'ext://sys.stdout',
            },
        },
        "loggers": {
            "prompt_generator": {
                'handlers': ['consoleHandler'],
                'level': "DEBUG",
            },
            "uvicorn": {
                'handlers': ['consoleHandler']
            },
            "uvicorn.access": {
                # Use the project logger to replace uvicorn.access logger
                'handlers': []
            }
        }
    }

    class Config:
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get settings object, and use cache to speed up the execution.

    Returns:
        object: The instance of the current used settings class.
    """
    base_settings = Settings()
    logger = logging.getLogger(base_settings.PROJECT_SLUG)
    return base_settings
