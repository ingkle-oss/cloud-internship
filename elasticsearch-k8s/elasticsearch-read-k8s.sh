#!/bin/bash

kubectl delete -f elasticsearch-read-k8s-pod.yaml -n pipelines

export SCRIPT=$1

envsubst < elasticsearch-read-k8s-pod.yaml | kubectl apply -n pipelines -f -