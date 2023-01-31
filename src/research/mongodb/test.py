import time
from functools import wraps
from pymongo import MongoClient, DESCENDING, cursor

mongodb = MongoClient(
            "mongodb://127.0.0.1:27017/?serverSelectionTimeoutMS=2000&directConnection=true")

stor = mongodb["movies"]["movies"]

def measure(func):
    @wraps(func)
    def inner(*args, **kwargs):
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            end = time.time()
            print(end - start)
            with open("log.txt", 'a', encoding='utf-8') as file:
                file.write(f"{str(end - start)}\n")

    return inner


@measure
def get_movie_by_id(movie_id: str):
    return stor.find({"_id": movie_id})


@measure
def get_movies_by_rating(rating: int):
    return stor.find({"rating": {"$gte": rating}})


@measure
def get_movies_by_rating_with_sort(rating: int):
    return stor.find({"rating": {"$gte": rating}}).sort("rating", direction=DESCENDING)


@measure
def get_movies_by_user_id(user_id: str):
    return stor.find({"scores.user_id": user_id}, {"_id": 1, "scores": 0, "rating": 0})


@measure
def add_score_to_movie(movie_id: str, user_id: str, score: int):
    stor.update_one(
        {"_id": movie_id},
        {"$addToSet": {"scores": {"user_id": user_id, "score": score}}},
    )


if __name__ == "__main__":
    get_movie_by_id("8595d967-92b8-4807-a71d-0585208823fd")
    get_movies_by_rating(6)
    get_movies_by_rating_with_sort(6)
    get_movies_by_user_id("0b29e1d0-e81f-4511-a0b4-7330f67f1f2f")
    add_score_to_movie("8595d967-92b8-4807-a71d-0585208823fd", "0b29e1d0-e81f-4511-a0b4-7330f67f1f2f", 5)
