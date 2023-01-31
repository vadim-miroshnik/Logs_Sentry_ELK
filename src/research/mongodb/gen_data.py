import time
import uuid
import pymongo
import random

mongodb = pymongo.MongoClient(
            "mongodb://127.0.0.1:27017/?serverSelectionTimeoutMS=2000&directConnection=true&readPreference=primary")

stor = mongodb["movies"]["movies"]

USERS_CNT = 10000
MOVIES_CNT = 100000
MIN_SCORE = 1
MAX_SCORE = 10
MAX_SCORES = 10000


user_ids = [str(uuid.uuid4()) for _ in range(USERS_CNT)]
movie_ids = [str(uuid.uuid4()) for _ in range(MOVIES_CNT)]


def add_to_mongo(movie: dict):
    stor.insert_one(movie)


def gen_movie(movie_id: str, scores: list[dict]):
    rating = 0
    if len(scores) > 0:
        rating = sum(s.get("score") for s in scores) / len(scores)
    return {
        "_id": movie_id,
        "scores": scores,
        "rating": rating
    }


def generate_data():
    count = 0
    for movie in movie_ids:
        scores = []
        for score in range(random.randint(0, MAX_SCORES)):
            scores.append({"user_id": random.choice(user_ids), "score": random.randint(MIN_SCORE, MAX_SCORE)})
        add_to_mongo(gen_movie(movie, scores))
        count += 1
    return count


if __name__ == "__main__":
    start = time.time()
    count = generate_data()
    end = time.time()
    print(end - start)
    print(count)
    with open("log.txt", 'a', encoding='utf-8') as file:
        file.write(f"Insert {count} movies = {str(end - start)}\n")