from typing import Optional

from aiokafka import AIOKafkaProducer

producer: AIOKafkaProducer | None = None


async def get_kafka_producer():
    return producer
