FROM bitnami/spark:3.5.4

USER root

RUN pip install redis

RUN mkdir -p /opt/bitnami/spark/jars/custom

COPY ./org.apache.spark_spark-sql-kafka-0-10_2.12-3.5.4.jar /opt/bitnami/spark/jars/custom/ 
COPY ./org.postgresql_postgresql-42.6.0.jar /opt/bitnami/spark/jars/custom/ 
COPY ./com.redislabs_spark-redis_2.12-3.1.0.jar /opt/bitnami/spark/jars/custom/

USER 1001