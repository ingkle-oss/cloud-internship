#!/bin/bash

kubectl delete -f deltastandalone-read-k8s-pod.yaml -n pipelines
kubectl apply -f deltastandalone-read-k8s-pod.yaml -n pipelines