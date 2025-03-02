#!/bin/bash

# Submit Debezium connector for MySQL
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" \
localhost:8083/connectors/ -d '{
  "name": "mysql-source",
  "config": {
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "tasks.max": "1",
    "database.hostname": "mysql",
    "database.port": "3306",
    "database.user": "debezium",
    "database.password": "dbz",
    "database.server.id": "2",
    "topic.prefix": "mysqltopic",
    "schema.history.internal.kafka.bootstrap.servers": "kafka:9092",
    "schema.history.internal.kafka.topic": "schema-changes.mariadb",
    "database.include.list": "mariadb"
  }
}'

# Submit Debezium connector for PostgreSQL
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" \
localhost:8083/connectors/ -d '{
  "name": "postgres-source",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "tasks.max": "1",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "postgres",
    "database.password": "123456",
    "database.server.id": "1",
    "topic.prefix": "postgrestopic",
    "database.dbname": "postgres",
    "table.whitelist": "public.customer",	
    "database.history.kafka.bootstrap.servers": "kafka1:9092",
    "database.history.kafka.topic": "schema-changes.postgres"
  }
}'
