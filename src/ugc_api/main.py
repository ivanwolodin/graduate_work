from contextlib import asynccontextmanager

import uvicorn
from aiokafka import AIOKafkaProducer
from api.v1 import content
from broker import kafka_broker
from broker.kafka_broker import KafkaProducer
from core.config import config
from fastapi import FastAPI

dependencies = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    aio_kafka_producer = AIOKafkaProducer(bootstrap_servers=f'{config.KAFKA_HOST}:{config.KAFKA_PORT}')
    await aio_kafka_producer.start()
    kafka_broker.kafka_producer = KafkaProducer(aio_kafka_producer)
    yield
    await kafka_broker.kafka_producer.producer.stop()


app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    dependencies=dependencies,
    lifespan=lifespan,
)

app.include_router(content.router, prefix='/api/v1/content', tags=['UGC'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
