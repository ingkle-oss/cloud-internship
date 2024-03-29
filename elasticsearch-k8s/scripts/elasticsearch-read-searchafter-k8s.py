from elasticsearch import Elasticsearch
import sys, time

username = sys.argv[1]
password = sys.argv[2]
host = 'elasticsearch-es-default.elasticsearch.svc.cluster.local'
port = 9200

es = Elasticsearch(hosts=[f'http://{username}:{password}@{host}:{port}'])
target_index = 'mytest'

resp = es.open_point_in_time(index=target_index, keep_alive='2m')

size = 10000
my_query = { 'match_all' : {} }
pit_clause = { 'id': resp['id'], 'keep_alive': '2m' }
sort_clause = [{'_shard_doc': 'asc'}]
search_after_clause = [-1]

total_time = 0
print('start...')

if es.indices.exists(index=target_index):
    while True:
        # data-reading code
        start = time.time()
        resp = es.search(size=size, query=my_query, pit=pit_clause, sort=sort_clause, search_after=search_after_clause)
        end = time.time()
        total_time = total_time + (end - start)
    
        if resp['hits']['hits'] == []:
            break
        
        for data in [hit['_source'] for hit in resp['hits']['hits']]:
            pass
        
        search_after_clause = resp['hits']['hits'][-1]['sort']
else:
    print(f'index \'{target_index}\' does not exist')
    exit(1)

print('Complete, Time elapsed(s): ', total_time)