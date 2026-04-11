FROM apache/airflow:2.8.1

USER root

ARG SPARK_VERSION=3.5.1
ARG HADOOP_VERSION=3

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl openjdk-17-jre-headless \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL \
      https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
      -o /tmp/spark.tgz \
    && tar -xzf /tmp/spark.tgz -C /opt \
    && mv /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark \
    && rm /tmp/spark.tgz

ENV SPARK_HOME=/opt/spark
ENV PATH="${SPARK_HOME}/bin:${PATH}"
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

USER airflow

RUN pip install --no-cache-dir apache-airflow-providers-apache-spark
