""""""

import time
from functools import wraps

import vertica_python

connection_info = {
    "host": "127.0.0.1",
    "port": 5433,
    "user": "dbadmin",
    "password": "",
    "database": "docker",
    "autocommit": False,
    "use_prepared_statements": True,
}


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
def execute_query(conn, query: str, show_result: bool = False):
    cursor = conn.cursor()
    cursor.execute(query)
    if show_result:
        for row in cursor.iterate():
            print(row)
    cursor.close()


if __name__ == "__main__":
    with vertica_python.connect(**connection_info) as conn:
        # 1
        query_count = "SELECT COUNT(*) FROM views"
        execute_query(conn, query_count, True)

        # 2
        query_unique_user = "SELECT COUNT(DISTINCT user_id) FROM views"
        execute_query(conn, query_unique_user, True)

        # 3
        query_unique_movie = "SELECT COUNT(DISTINCT movie_id) FROM views"
        execute_query(conn, query_unique_movie, True)

        # 4
        query_movie_by_user = "SELECT user_id, COUNT(movie_id) FROM views GROUP BY user_id"
        execute_query(conn, query_movie_by_user)

        # 5
        query_movie_user = "SELECT user_id, movie_id, COUNT(viewed_frame)/MAX(viewed_frame) FROM views GROUP BY user_id, movie_id"
        execute_query(conn, query_movie_user)

        # 6
        query_where = "SELECT COUNT(DISTINCT movie_id) FROM views WHERE event_time >= '2023-01-14 22:15:00'"
        execute_query(conn, query_where)
