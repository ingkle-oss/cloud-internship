import sys
from pyspark.sql import SparkSession
from pyspark.context import SparkContext
from delta import *
import time

if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} <access_key> <secret_key>")
    exit(1)

endpoint = 'minio.minio.svc.cluster.local'

def load_config(spark_context: SparkContext):
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.access.key', sys.argv[1])
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.secret.key', sys.argv[2])
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.path.style.access', 'true')
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.endpoint', endpoint)
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.connection.ssl.enabled', 'false')
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')

builder = SparkSession.builder \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
spark = configure_spark_with_delta_pip(builder).getOrCreate()
load_config(spark.sparkContext)

df = spark.read \
    .format("delta") \
    .load('s3a://delta/test100k')
    
def f(row):
    pass

print('Read delta...')
start = time.time()

#df.collect()
df.foreach(f)

end = time.time()
print('Read Complete, Time elapsed(s): ', end-start)