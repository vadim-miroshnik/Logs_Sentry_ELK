from functools import lru_cache

import pymongo
from fastapi import Depends
from services.bookmarks import BookmarksService
from services.movies import MoviesService
from services.reviews import ReviewsService
from storage.mongodb import Mongodb, get_collection

from core.config import settings

mongodb: pymongo.MongoClient | None = None

mongodb = pymongo.MongoClient(
    f"mongodb://{settings.mongo.host}:{settings.mongo.port}/?serverSelectionTimeoutMS=2000&directConnection=true"
)

# async def get_mongodb_client():
#    return mongodb


@lru_cache()
def get_mongodb_bookmarks(mongo: Mongodb = Depends(get_collection(mongodb, "movies", "bookmarks"))) -> BookmarksService:
    return BookmarksService(mongo)


@lru_cache()
def get_mongodb_movies(mongo: Mongodb = Depends(get_collection(mongodb, "movies", "movies"))) -> MoviesService:
    return MoviesService(mongo)


@lru_cache()
def get_mongodb_reviews(mongo: Mongodb = Depends(get_collection(mongodb, "movies", "reviews"))) -> ReviewsService:
    return ReviewsService(mongo)
