from pyspark.sql import SparkSession
from pyspark.context import SparkContext
from pyspark.sql.types import StructType
from delta import *
import time

accessKey = 'testuser'
secretKey = 'test1004'
endpoint = '10.0.0.155:9000'

def load_config(spark_context: SparkContext):
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.access.key', accessKey)
    spark_context._jsc.hadoopConfiguration().set('fs.s3a.secret.key', secretKey)
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

print('Loading csv...')
start = time.time()
df = spark.read.options(header=True, inferSchema=True) \
    .format("csv") \
    .load('s3a://test/test2.csv')
end = time.time()
print('Load Complete, Time elapsed: ', end-start)

print('Writing delta...')
start = time.time()
df.write.format('delta').mode("overwrite").save('s3a://delta/test2')
end = time.time()
print('Write Complete, Time elapsed: ', end - start)
