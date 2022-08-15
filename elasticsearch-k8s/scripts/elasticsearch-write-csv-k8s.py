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

# Write csv to Elasticsearch

if es.indices.exists(index="mytest"):
    print("index already exists")
else:
    es.indices.create(index="mytest")
    
    # write csv to Elasticsearch
    print('start...')
    start = time.time()

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
                helpers.bulk(es, data, index="mytest")
    
    end = time.time()
    print('Complete, Time elapsed(s): ', end-start)