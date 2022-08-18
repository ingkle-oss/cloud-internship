from pymongo import MongoClient
import sys, time

if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} <MongoDB username> <MongoDB password>")
    exit(1)

# MongoDB Connection Config

host = 'mongodb-mongos.mongodb.svc.cluster.local'
port = 27017
username = sys.argv[1]
password = sys.argv[2]
database = 'test_db'
coll = 'test_coll'

CONNECTION_STRING = 'mongodb://%s:%s@%s:%d/?authSource=admin' % (username, password, host, port)
conn = MongoClient(CONNECTION_STRING)

db = conn.get_database(database)
collection = db.get_collection(coll)

cursor = collection.find()
print("start...")

start = time.time()

for doc in cursor:
    pass
    
end = time.time()
print('Complete, Time elapsed(s): ', end-start)

conn.close()