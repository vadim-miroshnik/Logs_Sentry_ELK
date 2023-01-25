from typing import Generic, List, cast, Type, Tuple
from .interface import Storage, T
import pymongo


class Mongodb(Generic[T], Storage[T]):

    def __init__(self, mongodb: pymongo.MongoClient):
        self.mongodb = mongodb
        self.db = mongodb["movies"]

        cls = cast(Mongodb, self.__class__)
        if cls.__args:
            self.ref = cls.__args[0]

        self.coll = self.db[self.ref.__name__.lower()]
        print(self.coll)

    def __class_getitem__(cls, *args) -> Type["Mongodb"]:
        cls.__args = cast(Tuple[Type[T]], args)
        return super().__class_getitem__(*args)

    async def insert(self, item: T) -> None:
        id = self.coll.insert_one(item.__dict__).inserted_id
        print(id)

    async def insert_chunk(self, items: List[T], **kwargs) -> None:
        pass

    async def select(self, id: str) -> T:
        obj = self.coll.find_one({"user_id": id})
        print(obj)

    async def delete(self, id: str) -> bool:
        pass

    async def update(self, id: T) -> bool:
        pass

    async def select_items(self, query: str, fltr: dict, **kwargs) -> List[T]:
        pass
