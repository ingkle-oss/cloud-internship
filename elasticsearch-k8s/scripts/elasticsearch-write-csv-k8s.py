from elasticsearch import helpers, Elasticsearch
from smart_open import open
import boto3
import sys, time

# Minio Config

endpoint = 'minio.minio.svc.cluster.local'
bucket_name = 'test'
file_name = 'test.csv'

session = boto3.Session(
    aws_access_key_id=sys.argv[1],
    aws_secret_access_key=sys.argv[2]
)
client = session.client('s3', endpoint_url=f'http://{endpoint}')

# Elasticsearch config

host = 'elasticsearch-es-default.elasticsearch.svc.cluster.local'
port = 9200
username = sys.argv[3]
password = sys.argv[4]

es = Elasticsearch(hosts=[f'http://{username}:{password}@{host}:{port}'])
target_index = 'mytest'

if es.indices.exists(index=target_index):
    print("index already exists")
    es.indices.delete(index=target_index)
    print(f"index \'{target_index}\' is deleted")

es.indices.create(index=target_index)
print(f'index \'{target_index}\' is created')

# write csv to Elasticsearch
total_time = 0
print('start...')

with open(f's3://{bucket_name}/{file_name}', 'rb', encoding='utf-8', transport_params={'client':client}) as fin:
    header = fin.readline().rstrip().split(',')

    row = None
    while True:
        if row == '':
            break
    
        data = []
    
        # Read 10000 rows and write
        for _ in range(10000):
            row = fin.readline().rstrip()
        
            if row == '':
                break

            data.append(dict(zip(header, row.split(','))))
    
        if data != []:
            start = time.time()
            helpers.bulk(es, data, index=target_index)
            end = time.time()
            total_time = total_time + (end - start)

print('Complete, Time elapsed(s): ', total_time)