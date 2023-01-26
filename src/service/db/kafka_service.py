from functools import lru_cache

from aioredis import Redis
from fastapi import Depends
from aiokafka import AIOKafkaProducer
from db.redis import get_redis
from db.kafka import get_kafka_producer
from storage.kafka import KafkaService


@lru_cache()
def get_kafka_service(
    redis: Redis = Depends(get_redis),
    kafka: AIOKafkaProducer = Depends(get_kafka_producer),
) -> KafkaService:
    return KafkaService(redis, kafka)
