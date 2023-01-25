from typing import Optional
from functools import lru_cache
import pymongo
from fastapi import Depends
from models.events import ViewEvent
from storage.mongodb import Mongodb

mongodb: Optional[pymongo.MongoClient] = None


async def get_mongodb_client():
    return mongodb


@lru_cache()
def get_mongodb_view_events(
    mongo: pymongo.MongoClient = Depends(get_mongodb_client)
) -> Mongodb[ViewEvent]:
    return Mongodb[ViewEvent](mongo)