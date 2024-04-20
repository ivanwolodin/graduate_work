import json
from typing import Generator

from kafka.consumer.fetcher import ConsumerRecord
from models.content_model import BaseContent


class Transformer:
    def transform(self, data: Generator[ConsumerRecord, None, None]):
        return self.transform_json(data)

    def transform_json(self, messages) -> Generator[BaseContent, None, None]:
        for record in messages:
            user_id, content_type = record.key.decode("utf-8").split(":")
            content_data = json.loads(record.value.decode("utf-8"))
            yield BaseContent(
                user_id=user_id,
                content_type=content_type,
                object_id=content_data.get("object_id"),
                metrics=content_data.get("metrics"),
            )


def get_transformer():
    return Transformer()
