#!/bin/bash


docker cp ./redisSink.py spark:/opt/bitnami/spark


docker exec -it spark bash -c "spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4,com.redislabs:spark-redis_2.12:3.1.0 \
  ./redisSink.py"
