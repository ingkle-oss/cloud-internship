from elasticsearch import Elasticsearch
import sys, time

username = sys.argv[1]
password = sys.argv[2]
host = 'elasticsearch-es-default.elasticsearch.svc.cluster.local'
port = 9200

es = Elasticsearch(hosts=[f'http://{username}:{password}@{host}:{port}'])
target_index = 'mytest'
size = 10000
my_query = { 'match_all' : {} }

total_time = 0
print('start...')

if es.indices.exists(index=target_index):
    # data-reading code
    start = time.time()
    resp = es.search(index=target_index, size = size, query=my_query, scroll='2m')
    end = time.time()
    total_time = total_time + (end - start)
    
    for doc in resp['hits']['hits']:
        pass
        
    old_scroll_id = resp['_scroll_id']
    
    while len(resp['hits']['hits']) > 0:
        # data-reading code
        start = time.time()
        resp = es.scroll(scroll_id=old_scroll_id, scroll='2m')
        end = time.time()
        total_time = total_time + (end - start)

        for doc in resp['hits']['hits']:
            pass
            
        old_scroll_id = resp['_scroll_id']
    
else:
    print(f'index \'{target_index}\' does not exist')
    exit(1)

print('Complete, Time elapsed(s): ', total_time)