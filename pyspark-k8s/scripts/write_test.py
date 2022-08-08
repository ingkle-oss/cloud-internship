# %%
import sys
from pyspark.sql import SparkSession
from pyspark.context import SparkContext
from delta import *
from functools import reduce
import time

# %%
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

# %%
builder = SparkSession.builder \
    .master("local") \
    .appName("MyTest") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
spark = configure_spark_with_delta_pip(builder).getOrCreate()
load_config(spark.sparkContext)

# %%
print('Loading csv...')
start = time.time()

df = spark.read.options(header=True, inferSchema=True) \
    .format("csv") \
    .load('s3a://test/test.csv')
    
end = time.time()
print('Load Complete, Time elapsed: ', end-start)

# %%
current_columns = df.columns
new_columns = list(map(lambda item: item.replace(" ", "_"), current_columns))
final_df = reduce(lambda data, idx: data.withColumnRenamed(current_columns[idx], new_columns[idx]),
            range(len(current_columns)), df)

# %%
print('Writing delta...')
start = time.time()

final_df.write.format('delta').mode("overwrite").option("overwriteSchema", "true").save('s3a://delta/test')

end = time.time()
print('Write Complete, Time elapsed: ', end - start)