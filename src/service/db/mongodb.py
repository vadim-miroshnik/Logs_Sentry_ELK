from functools import lru_cache
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends
from services.bookmarks import BookmarksService
from services.movies import MoviesService
from services.reviews import ReviewsService
from storage.mongodb import Mongodb, get_collection

from core.config import settings


mongodb: AsyncIOMotorClient | None = None
mongodb = AsyncIOMotorClient(
    "mongodb://mongos1:27017/?serverSelectionTimeoutMS=2000&directConnection=true&uuidRepresentation=standard"
)


@lru_cache()
def get_mongodb_bookmarks(mongo: Mongodb = Depends(get_collection(mongodb, "movies", "bookmarks"))) -> BookmarksService:
    return BookmarksService(mongo)


@lru_cache()
def get_mongodb_movies(mongo: Mongodb = Depends(get_collection(mongodb, "movies", "movies"))) -> MoviesService:
    return MoviesService(mongo)


@lru_cache()
def get_mongodb_reviews(mongo: Mongodb = Depends(get_collection(mongodb, "movies", "reviews"))) -> ReviewsService:
    return ReviewsService(mongo)
