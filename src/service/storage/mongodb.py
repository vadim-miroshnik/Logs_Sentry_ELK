from typing import List
from .interface import Storage
import pymongo


class Mongodb(Storage):

    def __init__(self, mongodb: pymongo.MongoClient, db: str, coll: str):
        self.mongodb = mongodb
        self.db = db
        self.coll = coll

    async def insert(self, item: dict) -> dict:
        return self.mongodb[self.db][self.coll].insert_one(item)

    async def select(self, item: dict) -> dict:
        return self.mongodb[self.db][self.coll].find_one(item)

    async def delete(self, item: dict) -> None:
        return self.mongodb[self.db][self.coll].delete_one(item)

    async def update(self, item: dict, prop: dict) -> bool:
        return self.mongodb[self.db][self.coll].update_one(item, prop)

    async def select_items(self, fltr: dict, **kwargs) -> list:
        return self.mongodb[self.db][self.coll].find(fltr)


def get_collection(client: pymongo.MongoClient, db: str, coll: str) -> Mongodb:
    return Mongodb(client, db, coll)
