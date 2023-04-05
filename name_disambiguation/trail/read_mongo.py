from bson import ObjectId
from pymongo import MongoClient
import urllib.parse


def _connect_mongo(host, port, username, password, db, auth):
    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s?%s' % (username, password, host, port, db, auth)
        print(mongo_uri)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)
    return conn[db]


username = "aminer_hanhongbo"
password = "aminer@hanhongbo.com"

user = urllib.parse.quote_plus(username)
passwd = urllib.parse.quote_plus(password)

# db_yuan = _connect_mongo(username=user, password=passwd, host="192.168.6.208", port= )


db_yuan = _connect_mongo(host="192.168.6.208", port=37017, username=user, password=passwd, db='aminer',
                         auth="authSource=aminer")


# print(db_yuan.list_collection_names())

i = ['53e99784b7602d9701f3e139',
     '53e99784b7602d9701f3e174',
     '53e99784b7602d9701f3e174',
     '53e99784b7602d9701f3e174',
     '53e99784b7602d9701f3e174',
     '53e99784b7602d9701f3e174',
     '53e99784b7602d9701f3e174',
     '53e99784b7602d9701f3e17a',
     '53e99784b7602d9701f3e17a',
     '53e99784b7602d9701f3e17a',
     '53e99784b7602d9701f3e17a', ]

cursor_yuan = db_yuan["publication_dupl"].find({'_id': {"$in": list(map(lambda a: ObjectId(a), i))}})
print(list(cursor_yuan))
