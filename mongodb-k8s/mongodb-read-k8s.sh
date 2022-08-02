#!/bin/bash

kubectl delete -f mongodb-read-k8s-pod.yaml -n pipelines

export SCRIPT=$1

envsubst < mongodb-read-k8s-pod.yaml | kubectl apply -n pipelines -f -