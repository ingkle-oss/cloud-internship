# How to execute on K8s

## Create namespace and rbac

```
kubectl apply -k manifests
```

## Submit spark app on localhost.

### Prerequsites

```
pip install delta-spark==1.2.0
pip install pyspark==3.2.1
```

### Submit

```
./submit-spark.sh wordcount.py wordcount.py
```

## Submit spark app on K8s.

```
./submit-spark-k8s.sh /opt/spark/examples/src/main/python/wordcount.py /opt/spark/examples/src/main/python/wordcount.py
```
