CREATE DATABASE analysis;

CREATE DATABASE shard;

CREATE DATABASE replica;

CREATE TABLE shard.views (
	`id` UInt64,
    `user_id` String,
    `movie_id` String,
    `viewed_frame` UInt64,
    `event_time` DateTime
) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/views', 'replica_1')
PARTITION BY toYYYYMMDD(event_time)
ORDER BY id;

CREATE TABLE replica.views (
	`id` UInt64,
    `user_id` String,
    `movie_id` String,
    `viewed_frame` UInt64,
    `event_time` DateTime
) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/views', 'replica_2')
PARTITION BY toYYYYMMDD(event_time)
ORDER BY id;

CREATE TABLE analysis.views (
	`id` UInt64,
    `user_id` String,
    `movie_id` String,
    `viewed_frame` UInt64,
    `event_time` DateTime
) ENGINE = Distributed('company_cluster', '', views, rand());