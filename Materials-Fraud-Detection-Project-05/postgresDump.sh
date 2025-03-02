#!/bin/bash

# Create the database
docker exec -it postgres psql -U postgres -c "CREATE DATABASE postgresql_dump;"

docker cp ./postgresSink.py spark:/opt/bitnami/spark


docker exec -it spark bash -c "spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4,org.postgresql:postgresql:42.6.0 \
  ./postgresSink.py"
