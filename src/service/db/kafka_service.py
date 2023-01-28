from functools import lru_cache

from fastapi import Depends
from aiokafka import AIOKafkaProducer
from db.kafka import get_kafka_producer
from storage.kafka import KafkaService


@lru_cache()
def get_kafka_service(
    kafka: AIOKafkaProducer = Depends(get_kafka_producer),
) -> KafkaService:
    return KafkaService(kafka)
