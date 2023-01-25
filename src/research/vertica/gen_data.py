""""""

import time
import uuid
import random
from datetime import datetime
import vertica_python
from tqdm.contrib.concurrent import process_map


user_ids = [str(uuid.uuid4()) for _ in range(100)]
movie_ids = [str(uuid.uuid4()) for _ in range(1000)]
max_len = 3 * 60 * 60

connection_info = {
    "host": "127.0.0.1",
    "port": 5433,
    "user": "dbadmin",
    "password": "",
    "database": "docker",
    "autocommit": False,
    "use_prepared_statements": True,
}


def create_views_table():
    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS views (
            id IDENTITY,
            user_id VARCHAR(36) NOT NULL,
            movie_id VARCHAR(36) NOT NULL,
            viewed_frame INTEGER NOT NULL,
            event_time DATETIME NOT NULL
        );
        """
        )
        cursor.execute("DELETE FROM views")
        connection.commit()

def gen_event() -> tuple:
    event = (
        random.choice(user_ids),
        random.choice(movie_ids),
        random.randint(1, max_len),
        datetime.now(),
    )
    return event


def gen_events(prm):
    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()
        events = [gen_event() for _ in range(1000)]
        # start = time.time()
        try:
            cursor.executemany(
                "INSERT INTO views (user_id, movie_id, viewed_frame, event_time) VALUES (?, ?, ?, ?)",
                events,
            )
        except Exception as e:
            raise e
        cursor.close()
        connection.commit()
        # end = time.time()
        # print(end - start)


def generate_data():
    start = time.time()
    process_map(gen_events, range(0, 10000), max_workers=4, chunksize=1)
    end = time.time()
    print(end - start)
    with open("log.txt", 'a', encoding='utf-8') as file:
        file.write(f"Insert 10000000 events = {str(end - start)}\n")


if __name__ == "__main__":
    create_views_table()
    generate_data()
