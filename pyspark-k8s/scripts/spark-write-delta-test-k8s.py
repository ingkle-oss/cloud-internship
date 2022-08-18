from pyspark.sql import SparkSession
from pyspark.context import SparkContext
import pandas as pd
from smart_open import open
from delta import *
import boto3
import time, sys

if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} <access_key> <secret_key>")
    exit(1)

# Minio Config

endpoint = 'minio.minio.svc.cluster.local'
username = sys.argv[1]
password = sys.argv[2]
bucket_name = 'test'
file_name = 'test.csv'

session = boto3.Session(
    aws_access_key_id=sys.argv[1],
    aws_secret_access_key=sys.argv[2]
)
client = session.client('s3', endpoint_url=f'http://{endpoint}')

# delta Config

def load_config(spark_context: SparkContext):
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.access.key', username)
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.secret.key', password)
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.path.style.access', 'true')
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.endpoint', endpoint)
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.connection.ssl.enabled', 'false')
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')

builder = SparkSession.builder \
    .master("local") \
    .appName("MyTest") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
spark = configure_spark_with_delta_pip(builder).getOrCreate()
load_config(spark.sparkContext)

####################################

total_time = 0
print("start...")

with open(f's3://{bucket_name}/{file_name}', 'rb', encoding='utf-8', transport_params={'client':client}) as fin:
    header = fin.readline().rstrip().split(',')
    
    row = None
    while True:
        if row == '':
            break
        
        rows = []
        
        # Read 10000 rows and write
        for _ in range(10000):
            row = fin.readline().rstrip()
            
            if row == '':
                break

            rows.append(row.split(','))
        
        if rows != []:
            data = dict(zip(header, list(zip(*rows))))
            df = spark.createDataFrame(pd.DataFrame(data))
            
            start = time.time()
            df.write.format('delta').mode('append').save('s3a://delta/test/')
            end = time.time()
            
            total_time = total_time + (end-start)
            
print('Complete, Time elapsed(s): ', total_time)