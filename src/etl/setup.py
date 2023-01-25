from clickhouse_driver import Client
from sql import SQL_table, SQL_kafka, SQL_view

if __name__ == "__main__":
    client = Client(host='localhost')
    client.execute(SQL_table)
    client.execute(SQL_kafka)
    client.execute(SQL_view)
