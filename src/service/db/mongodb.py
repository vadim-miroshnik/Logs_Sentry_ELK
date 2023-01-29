from functools import lru_cache
import pymongo
from fastapi import Depends
from storage.mongodb import Mongodb, get_collection
from services.bookmarks import BookmarksService

mongodb: pymongo.MongoClient | None = None

mongodb = pymongo.MongoClient(
        "mongodb://mongos1:27017/?serverSelectionTimeoutMS=2000&directConnection=true")
# async def get_mongodb_client():
#    return mongodb


@lru_cache()
def get_mongodb_bookmarks(
    mongo: Mongodb = Depends(get_collection(mongodb, "movies", "bookmarks"))
) -> BookmarksService:
    return BookmarksService(mongo)
