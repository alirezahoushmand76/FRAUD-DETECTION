#!/bin/bash


docker cp ./process.py spark:/opt/bitnami/spark


docker exec -it spark bash -c "spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4 ./process.py"
