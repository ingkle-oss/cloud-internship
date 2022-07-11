#!/bin/bash

HADOOP_VERSION=${HADOOP_VERSION:-3.3.1}
DELTALAKE_VERSION=${DELTALAKE_VERSION:-1.2.0}
DELTASHARING_VERSION=${DELTASHARING_VERSION:-0.5.0}
SPARK_SQL_KAFKA_VERSION=${SPARK_SQL_KAFKA_VERSION:-3.2.1}

DELTALAKE_JARS=${DELTALAKE_JARS:-}

if [ -z ${DELTALAKE_JARS} ]; then
    spark-submit \
        --packages org.apache.hadoop:hadoop-aws:${HADOOP_VERSION},org.apache.hadoop:hadoop-cloud-storage:${HADOOP_VERSION},io.delta:delta-core_2.12:${DELTALAKE_VERSION},io.delta:delta-sharing-spark_2.12:${DELTASHARING_VERSION},org.apache.spark:spark-sql-kafka-0-10_2.12:${SPARK_SQL_KAFKA_VERSION} \
        $@
else
    spark-submit \
        --packages org.apache.hadoop:hadoop-aws:${HADOOP_VERSION},org.apache.hadoop:hadoop-cloud-storage:${HADOOP_VERSION},org.apache.spark:spark-sql-kafka-0-10_2.12:${SPARK_SQL_KAFKA_VERSION} \
        --jars ${DELTALAKE_JARS} \
        $@
fi