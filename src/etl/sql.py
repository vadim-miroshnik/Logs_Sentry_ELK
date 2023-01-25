SQL_table = """
    CREATE TABLE views(
        user_uuid UUID,
        movie_uuid UUID,
        frame UInt32
    ) Engine = MergeTree
    ORDER BY (movie_uuid, user_uuid, frame);
"""

SQL_kafka = """
    CREATE TABLE views_queue(
        user_uuid UUID,
        movie_uuid UUID,
        frame UInt32
    )
    ENGINE = Kafka('broker:29092', 'views', 'clickhouse', 'JSONEachRow')
    SETTINGS kafka_skip_broken_messages = 5,
            kafka_thread_per_consumer = 0, 
            kafka_num_consumers = 1;
"""

SQL_view = """
    CREATE MATERIALIZED VIEW views_queue_mv TO views AS
        SELECT user_uuid, movie_uuid, frame
        FROM views_queue;
"""
