from aiokafka import AIOKafkaProducer

queues: dict = {}


class KafkaService:
    def __init__(self, producer: AIOKafkaProducer):
        self.producer = producer

    async def send(self, topic, key, value):
        if topic in queues:
            queues[topic] = queues[topic] + 1
        else:
            queues[topic] = 1
        await self.producer.send(
            topic=topic,
            value=str(value).encode(),
            key=str(key).encode(),
        )
