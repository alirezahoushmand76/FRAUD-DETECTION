#!/bin/bash

# Create Kafka topics
docker exec kafka ./bin/kafka-topics.sh --create --topic notification-postgres --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1

docker exec kafka ./bin/kafka-topics.sh --create --topic notification-mysql --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1

# Copy the Spark job to the Spark container
docker cp ./kafkaSink.py spark:/opt/bitnami/spark

# Execute the Spark job
docker exec -it spark bash -c "spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4 ./kafkaSink.py"