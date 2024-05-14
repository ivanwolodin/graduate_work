from confluent_kafka import Consumer, KafkaError
import requests

from config import get_settings

settings = get_settings()

# Configure Kafka consumer
conf = {
    'bootstrap.servers': 'your_kafka_broker',
    'group.id': 'your_consumer_group_id',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['your_kafka_topic'])

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        # Process received message
        user_id = msg.key().decode('utf-8')
        prompt = msg.value().decode('utf-8')

        # Make request to AI model
        response = requests.post(settings.GIGACHAT_API, json={'user_id': user_id, 'prompt': prompt})

        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

        payload = 'scope=GIGACHAT_API_PERS'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': 'идентификатор_запроса',
            'Authorization': 'Basic <авторизацонные_данные>'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        # Process response from AI model
        if response.status_code == 200:
            result = response.json()
            print("AI Model Response:", result)
        else:
            print("Error:", response.text)

except KeyboardInterrupt:
    pass

finally:
    # Close Kafka consumer
    consumer.close()