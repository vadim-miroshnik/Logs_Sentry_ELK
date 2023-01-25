""""""

import itertools
import threading
import uuid
from collections import OrderedDict

import numpy as np
from faker import Faker
from transliterate import get_translit_function

from view import View

locales = OrderedDict([("ru-RU", 1)])
fake = Faker(locales)

translit_ru = get_translit_function("ru")

# qty of users
users_all = 4

# qty of movies
movies_all = 2

# max and min length of movie in frames(frame = 1 sec)
min_len = 2 * 60 * 60
max_len = 3 * 60 * 60


def gen_users() -> dict:
    users = dict()

    # todo: get from users DB
    for _ in range(users_all):
        name = fake.last_name()
        login = translit_ru(name, reversed=True)
        login = login.replace("'", "")
        users[uuid.uuid4()] = login.lower()
    return users


def get_movies() -> list:
    movies = list()

    # todo: get from movies DB
    for _ in range(movies_all):
        movies.append(uuid.uuid4())


def gen_events(users: dict, movies: list) -> list:
    events = list()
    for i, (k, v) in enumerate(users.items()):
        for movie in movies:
            movie_len = np.random.randint(min_len, max_len)

            # qty of attempts to view movie (max 5)
            attempts = sorted(
                np.random.randint(0, movie_len, size=np.random.randint(1, 5)).tolist()
            )
            for i in range(len(attempts) - 1):
                for frame in range(attempts[i : i + 2][0], attempts[i : i + 2][1]):
                    view = View(user_id=k, movie_id=movie, viewed_frame=frame)
                    events.append(view)
                    # todo: send to Kafka queue


def run_gen_events(users: dict, movies: list, threads: int = 2):
    # divide users between threads
    part = int(len(users) / threads)
    usrs = [
        dict(itertools.islice(users.items(), i * part, (i + 1) * part))
        for i in range(threads)
    ]

    for user in usrs:
        t = threading.Thread(target=gen_events, args=(user, movies))
        t.daemon = True
        t.start()


if __name__ == "__main__":
    users = gen_users()
    movies = gen_users()
    run_gen_events(users, movies)
