import pika

from config import get_settings

settings = get_settings()


connection = pika.BlockingConnection(
    pika.ConnectionParameters(settings.RABBIT_SERVER)
)
channel = connection.channel()
channel.queue_declare(queue=settings.RABBIT_UGC_QUEUE)

message = 'user_id: ["film_id1"]'

channel.basic_publish(
    exchange='',
    routing_key=settings.RABBIT_UGC_QUEUE,
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent
    )
)

