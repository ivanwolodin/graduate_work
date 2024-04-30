import json
from uuid import UUID

import pika
import requests
from pydantic import BaseModel

from config import get_settings


class UGCData(BaseModel):
    user_id: UUID
    liked_movies: list[UUID]
    disliked_movies: list[UUID]


def callback(ch, method, properties, body):
    # Декодирование JSON-сообщения
    data = UGCData.model_validate_json(json.loads(body))
    user_id = data.user_id
    liked_movies_ids = data.liked_movies
    liked_movies_names = []
    for movie_id in liked_movies_ids:
        response_api = requests.get(
            f'https://{settings.MOVIES_API}{movie_id}')
        data = response_api.text
        parse_json = json.loads(data)
        liked_movies_names.append(parse_json['title'])

    # Генерация запроса для ИИ модели
    prompt = (f"Пользователю {user_id} нравятся фильмы: "
              f"{', '.join(liked_movies_names)}. "
              f"Посоветуй для этого пользователя 10 фильмов"
              f" с названием и годом !в формате json")
    print(prompt)
    # Отправка запроса в другую очередь
    channel.basic_publish(
        exchange='',
        routing_key='prompt_queue',
        body=prompt
    )

    print(f" [x] Sent prompt: {prompt}")


settings = get_settings()

connection = pika.BlockingConnection(
    pika.ConnectionParameters(settings.RABBIT_SERVER)
)
channel = connection.channel()
channel.queue_declare(queue='prompt_queue')

channel.basic_consume(
    queue=settings.RABBIT_UGC_QUEUE,
    on_message_callback=callback,
    auto_ack=True
)
