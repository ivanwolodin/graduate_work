import json
from typing import Generator

from kafka.consumer.fetcher import ConsumerRecord
from core.config import config


class Transformer:
    def transform(self, data: Generator[ConsumerRecord, None, None]):
        return self.transform_json(data)

    def transform_json(self, messages) -> Generator[dict, None, None]:
        for record in messages:
            prompts = []
            for user_likes in json.loads(record.value.decode("utf-8")):
                for likes in [user_likes] if type(user_likes) is dict else user_likes:
                    for user_id, user_likes in likes.items():
                        likes_text = ",".join(user_likes)
                        prompts.append({user_id: f"{config.RECSYS_PROMPT_PREFIX_SCRIPT} {likes_text} "
                                                 f"{config.RECSYS_PROMPT_POSTFIX_SCRIPT}"})
            yield prompts


def get_transformer():
    return Transformer()
