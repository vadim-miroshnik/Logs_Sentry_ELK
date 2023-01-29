from aiokafka import AIOKafkaProducer

class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Queues(dict, metaclass=Singleton):
    pass


queues = Queues()


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
