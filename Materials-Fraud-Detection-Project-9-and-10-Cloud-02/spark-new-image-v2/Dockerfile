FROM bitnami/spark:3.5.4

USER root

RUN pip install redis && \
    mkdir -p /opt/bitnami/spark/jars/custom

COPY ./jars/ /opt/bitnami/spark/jars/custom/ 

USER 1001