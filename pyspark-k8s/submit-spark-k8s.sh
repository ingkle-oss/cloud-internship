#!/bin/bash

PYTHON_SOURCE=${1:-/opt/spark/examples/src/main/python/wordcount.py} && shift

SPARK_IMAGE=${SPARK_IMAGE:-"jm3015/spark-py:latest"}
SPARK_DRIVER_MEMORY=${SPARK_DRIVER_MEMORY:-2g}
SPARK_EXECUTOR_INSTANCES=${SPARK_EXECUTOR_INSTANCES:-1}
SPARK_EXECUTOR_CORES=${SPARK_EXECUTOR_CORES:-1}
SPARK_EXECUTOR_MEMORY=${SPARK_EXECUTOR_MEMORY:-4g}
SPARK_NAMESPACE=${SPARK_NAMESPACE:-pipelines}
SPARK_SERVICEACCOUNTNAME=${SPARK_SERVICEACCOUNTNAME:-pipelines}
SPARK_EXTRA_CLASSPATH=${SPARK_EXTRA_CLASSPATH:-}
K8S_MASTER=${K8S_MASTER:-$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}')}

BASENAME=$(basename -- ${PYTHON_SOURCE})
FILENAME="${BASENAME%.*}"

spark-submit --master k8s://${K8S_MASTER} \
    --deploy-mode cluster \
    --name ${FILENAME} \
    --conf spark.driver.memory=${SPARK_DRIVER_MEMORY} \
    --conf spark.executor.instances=${SPARK_EXECUTOR_INSTANCES} \
    --conf spark.executor.cores=${SPARK_EXECUTOR_CORES} \
    --conf spark.executor.memory=${SPARK_EXECUTOR_MEMORY} \
    --conf spark.kubernetes.namespace=${SPARK_NAMESPACE} \
    --conf spark.kubernetes.driver.label.spark-app=${FILENAME} \
    --conf spark.kubernetes.container.image=${SPARK_IMAGE} \
    --conf spark.kubernetes.container.image.pullPolicy=Always \
    --conf spark.kubernetes.authenticate.driver.serviceAccountName=${SPARK_SERVICEACCOUNTNAME} \
    --conf spark.kubernetes.authenticate.executor.serviceAccountName=${SPARK_SERVICEACCOUNTNAME} \
    --conf spark.driver.extraClassPath=${SPARK_EXTRA_CLASSPATH} \
    --conf spark.executor.extraClassPath=${SPARK_EXTRA_CLASSPATH} \
    local://${PYTHON_SOURCE} $@
