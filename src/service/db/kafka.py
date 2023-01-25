from typing import Optional

from aiokafka import AIOKafkaProducer

producer: Optional[AIOKafkaProducer] = None


async def get_kafka_producer():
    return producer
