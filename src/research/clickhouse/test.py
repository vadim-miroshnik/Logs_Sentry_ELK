""""""

import time
from functools import wraps
import clickhouse_driver

client = clickhouse_driver.Client(host='localhost')


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
def execute_query(query: str):
    client.execute(query)


if __name__ == "__main__":
    # 1
    query_count = "SELECT COUNT(*) FROM analysis.views"
    execute_query(query_count)

    # 2
    query_unique_user = "SELECT uniqExact(user_id) FROM analysis.views"
    execute_query(query_unique_user)

    # 3
    query_unique_movie = "SELECT uniqExact(movie_id) FROM analysis.views"
    execute_query(query_unique_movie)

    # 4
    query_movie_by_user = "SELECT user_id, uniqExact(movie_id) FROM analysis.views GROUP BY user_id"
    execute_query(query_movie_by_user)

    # 5
    query_movie_user = "SELECT user_id, movie_id, COUNT(viewed_frame)/MAX(viewed_frame) FROM analysis.views GROUP BY user_id, movie_id"
    execute_query(query_movie_user)

    # 6
    query_where = "SELECT uniqExact(movie_id) FROM analysis.views WHERE event_time >= '2023-01-14 22:15:00'"
    execute_query(query_where)