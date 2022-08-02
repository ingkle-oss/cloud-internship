#!/bin/bash

kubectl delete -f mongodb-write-k8s-pod.yaml -n pipelines

export SCRIPT=$1

envsubst < mongodb-write-k8s-pod.yaml | kubectl apply -n pipelines -f -