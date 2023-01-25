""""""

import time
import random
import uuid
from datetime import datetime
import clickhouse_driver

client = clickhouse_driver.Client(host='localhost')

user_ids = [str(uuid.uuid4()) for _ in range(100)]
movie_ids = [str(uuid.uuid4()) for _ in range(1000)]
max_len = 3 * 60 * 60


def generate_data():
    events = list()
    for i in range(1, 10000001):
        event = {
            'id': i,
            'user_id': random.choice(user_ids),
            'movie_id': random.choice(movie_ids),
            'viewed_frame': random.randint(1, max_len),
            'event_time': datetime.now()
        }
        events.append(event)

        if len(events) >= 1000:
            try:
                client.execute('INSERT INTO analysis.views VALUES', events)
            except clickhouse_driver.errors.Error as e:
                print(f"insert error {e.code} - {e.message}")
            finally:
                events = []


if __name__ == "__main__":
    start = time.time()
    generate_data()
    end = time.time()
    print(end - start)
    with open("log.txt", 'a', encoding='utf-8') as file:
        file.write(f"Insert 10000000 events = {str(end - start)}\n")
