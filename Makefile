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
	docker-compose -f docker-compose.yml -f docker-compose_kafka.yml -f docker-compose.override.yml up --build ugc

down:
	docker-compose -f docker-compose.yml -f docker-compose_kafka.yml -f docker-compose_clickhouse.yml down

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
