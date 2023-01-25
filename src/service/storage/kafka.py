from typing import Generic, List, cast, Type, Tuple
from .interface import Storage, T
from aiokafka import AIOKafkaProducer


class Kafka(Generic[T], Storage[T]):

    def __init__(self, producer: AIOKafkaProducer):
        self.producer = producer

        cls = cast(Kafka, self.__class__)
        if cls.__args:
            self.ref = cls.__args[0]

        self.topic = self.ref.__name__.lower()

    def __class_getitem__(cls, *args) -> Type["Kafka"]:
        cls.__args = cast(Tuple[Type[T]], args)
        return super().__class_getitem__(*args)

    async def insert(self, item: T) -> None:
        await self.producer.send(
            topic=self.topic,
            value=str(item.viewed_frame).encode(),
            key=f"{item.user_id}+{item.movie_id}".encode(),
        )

    async def insert_chunk(self, items: List[T], **kwargs) -> None:
        pass

    async def select(self, id: str) -> T:
        pass

    async def delete(self, id: str) -> bool:
        pass

    async def update(self, id: T) -> bool:
        pass

    async def select_items(self, query: str, fltr: dict, **kwargs) -> List[T]:
        pass
