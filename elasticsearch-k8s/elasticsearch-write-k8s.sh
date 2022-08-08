#!/bin/bash

kubectl delete -f elasticsearch-write-k8s-pod.yaml -n pipelines

export SCRIPT=$1

envsubst < elasticsearch-write-k8s-pod.yaml | kubectl apply -n pipelines -f -