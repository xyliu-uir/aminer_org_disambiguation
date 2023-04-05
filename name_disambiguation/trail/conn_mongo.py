import pymongo
from urllib.parse import quote_plus
from bson import ObjectId


def connect(host, username, password, port, db, auth):
    if username and password:
        uri = "mongodb://%s:%s@%s:%s/%s?%s" % (username, password, host, port, db, auth)
        conn = pymongo.MongoClient(uri)
    else:
        conn = pymongo.MongoClient(host, port)

    return conn[db]


username = quote_plus("aminer_hanhongbo")
password = quote_plus("aminer@hanhongbo.com")

db_source = connect(host="192.168.6.208", username=username, password=password, port=37017, db="aminer",
                    auth="authSource=aminer")

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
     '53e99784b7602d9701f3e17a']

cursor = db_source["publication_dupl"].find({"_id": {"$in": list(map(lambda a: ObjectId(a), i))}})
print(list(cursor))