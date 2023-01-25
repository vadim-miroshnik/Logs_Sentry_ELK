from kafka import KafkaProducer
from kafka import KafkaConsumer
from time import sleep
import itertools
import threading
import uuid
from collections import OrderedDict
import json

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

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))


def gen_users() -> dict:
    users = dict()

    # todo: get from users DB
    for _ in range(users_all):
        name = fake.last_name()
        login = translit_ru(name, reversed=True)
        login = login.replace("'", "")
        users[uuid.uuid4()] = login.lower()
    return users


def get_movies_from_file(filename: str) -> list:
    with open(filename) as file:
        movies = [line.rstrip() for line in file]

    return movies


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
                    # view = View(user_id=k, movie_id=movie, viewed_frame=frame)
                    # events.append(view)
                    value = {
                        "user_uuid": str(k),
                        "movie_uuid": str(movie),
                        "frame": frame,
                    }
                    producer.send(
                        topic='views',
                        value=value,
                    )

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


def get_messages():
    consumer = KafkaConsumer(
        'views',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        group_id='echo-messages-to-stdout',
    )

    for message in consumer:
        print(message.key)


if __name__ == "__main__":
    movies = get_movies_from_file("data_generator/id_films.txt")
    users = gen_users()
    # run_gen_events(users, movies[0:10])
    gen_events(users, movies[0:10])
    # get_messages()


