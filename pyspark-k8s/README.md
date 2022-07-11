# How to execute on localhost

## Prerequsites

```
pip install delta-spark==1.2.0
pip install pyspark==3.2.1
```

## Submit spark app

```
./submit-spark.sh wordcount.py wordcount.py
```

# How to execute on K8s

## Create namespace and rbac

```
kubectl apply -k manifests
```

## Submit spark app

```
./submit-spark-k8s.sh /opt/spark/examples/src/main/python/wordcount.py /opt/spark/examples/src/main/python/wordcount.py
```
