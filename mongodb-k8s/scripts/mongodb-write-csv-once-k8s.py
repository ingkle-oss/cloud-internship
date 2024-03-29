from pymongo import MongoClient
from smart_open import open
import boto3
import sys, time, csv

if len(sys.argv) < 5:
    print(f"Usage: {sys.argv[0]} <Minio access key> <Minio secret key> <MongoDB username> <MongoDB password>")
    exit(1)

# Minio Config

endpoint = 'minio.minio.svc.cluster.local'
bucket_name = 'test'
file_name = 'test.csv'

session = boto3.Session(
    aws_access_key_id=sys.argv[1],
    aws_secret_access_key=sys.argv[2]
)
client = session.client('s3', endpoint_url=f'http://{endpoint}')

# MongoDB Connection Config

host = 'mongodb-mongos.mongodb.svc.cluster.local'
port = 27017
username = sys.argv[3]
password = sys.argv[4]
database = 'test_db'
coll = 'test_coll'

CONNECTION_STRING = 'mongodb://%s:%s@%s:%d/?authSource=admin' % (username, password, host, port)
conn = MongoClient(CONNECTION_STRING)

db = conn.get_database(database)
collection = db.get_collection(coll)
db.drop_collection(collection)

total_time = 0
print("start...")

with open(f's3://{bucket_name}/{file_name}', 'rb', encoding='utf-8', transport_params={'client':client}) as fin:
    data = csv.DictReader(fin)
    
    start = time.time()
    collection.insert_many(data)
    end = time.time()
    
    total_time = total_time + (end - start)

print('Complete, Time elapsed(s): ', total_time)