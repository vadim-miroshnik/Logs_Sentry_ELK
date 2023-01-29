run_click_house :
	docker-compose -f docker-compose.yml -f docker-compose_clickhouse.yml -f docker-compose_kafka.yml up -d \
		zookeeper_ch \
		clickhouse-node1 \
		clickhouse-node2 \
		clickhouse-node3 \
		clickhouse-node4

run_kafka:
	docker-compose -f docker-compose.yml -f docker-compose_kafka.yml -f docker-compose_clickhouse.yml up -d \
		zookeeper \
		broker \
		schema-registry \
		connect \
		control-center \
		ksqldb-server \
		ksqldb-cli \
		ksql-datagen \
		rest-proxy

run_environment: run_click_house run_kafka

run_ugc:
	docker-compose -f docker-compose.yml \
	-f docker-compose_kafka.yml \
	-f docker-compose_mongodb.yml \
	-f docker-compose.override.yml \
    up --build ugc

run_mongodb:
	docker-compose -f docker-compose_mongodb.yml up -d
	docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongosh'
	docker exec -it mongocfg1 bash -c 'echo "rs.status()" | mongosh'
	docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongosh'
	docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'
	docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongosh'
	docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongosh'
	docker exec -it mongors1n1 bash -c 'echo "use movies" | mongosh'
	docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"movies\")" | mongosh'

down:
	docker-compose -f docker-compose.yml -f docker-compose_kafka.yml -f docker-compose_clickhouse.yml -f docker-compose_mongodb.yml down

logs:
	docker-compose -f docker-compose.yml -f docker-compose_kafka.yml -f docker-compose_clickhouse.yml logs -f

prepare:
	pip3 install -r requirements.txt
	cp .env.example .env

setup_etl:
	python ./src/etl/setup.py

gen_views:
	python ./src/gen_events/gen_views.py

run_prod: run_environment
	docker-compose -f docker-compose.yml -f docker-compose_kafka.yml up -d --build ugc nginx
