from pymongo import MongoClient
import urllib.parse


# def get_database():
#     CONNECTION_STRING = 'mongodb://aminer_hanhongbo:aminer@hanhongbo.com@192.168.6.208:37017/aminer'
#
#     username = urllib.parse.quote_plus("aminer_hanhongbo")
#     password = urllib.parse.quote_plus("aminer@hanhongbo.com")
#
#     NEW_CONNECTION_STRING = f"mongodb://{username}:{password}@192.168.6.208:37017/aminer"


# uri = 'mongodb://aminer_hanhongbo:aminer@hanhongbo.com@192.168.6.208:37017/aminer'
#
# username = urllib.parse.quote_plus("aminer_hanhongbo")
# password = urllib.parse.quote_plus("aminer@hanhongbo.com")
#
# new_uri = f"mongodb://{username}:{password}@192.168.6.208:37017/aminer"
#
# client = MongoClient(new_uri)
#
# db = client.aminer
# collection = db.publication_dupl

# Connecting databases and make sure the connectiones exist.
import pymongo
import os

uri = 'mongodb://aminer_hanhongbo:aminer@hanhongbo.com@192.168.6.208:37017/aminer?authSource=aminer'

username = urllib.parse.quote_plus("aminer_hanhongbo")
password = urllib.parse.quote_plus("aminer@hanhongbo.com")

new_uri = f"mongodb://{username}:{password}@192.168.6.208:37017/aminer?authSource=aminer"


myclient = MongoClient(new_uri)

# mydb = myclient["mydatabase"]

print(myclient.list_database_names())

# dblist = myclient.list_database_names()
#
# if "mydatabase" in dblist:
#     print("The database exists.")
#
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#
# mydb = myclient["mydatabase"]
#
# mycol = mydb["customers"]
#
# collist = mydb.list_collection_names()
#
# if "customers" in collist:
#     print("The collection exists.")
#
# # insert data to customers.
#
# import pymongo
#
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["mydatabase"]
# mycol = mydb["customers"]
#
# mylist = [
#     {"name": "Amy", "address": "Apple st 652"},
#     {"name": "Hannah", "address": "Mountain 21"},
#     {"name": "Michael", "address": "Valley 345"},
#     {"name": "Sandy", "address": "Ocean blvd 2"},
#     {"name": "Betty", "address": "Green Grass 1"},
#     {"name": "Richard", "address": "Sky st 331"},
#     {"name": "Susan", "address": "One way 98"},
#     {"name": "Vicky", "address": "Yellow Garden 2"},
#     {"name": "Ben", "address": "Park Lane 38"},
#     {"name": "William", "address": "Central st 954"},
#     {"name": "Chuck", "address": "Main Road 989"},
#     {"name": "Viola", "address": "Sideway 1633"}
# ]
#
# x = mycol.insert_many(mylist)
#
# # print list of the _id values of the inserted documents:
# print(x.inserted_ids)
#
# # find one
# import pymongo
#
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["mydatabase"]
# mycol = mydb["customers"]
#
# x = mycol.find_one()
#
# print(x)
#
# # find all
# import pymongo
#
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["mydatabase"]
# mycol = mydb["customers"]
#
# for x in mycol.find():
#     print(x)
#
# # Find document(s) with the address "Park Lane 38":
# import pymongo
#
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["mydatabase"]
# mycol = mydb["customers"]
#
# myquery = {"address": "Park Lane 38"}
#
# mydoc = mycol.find(myquery)
#
# for x in mydoc:
#     print(x)
#
# # Sort the result alphabetically by name:
# import pymongo
#
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["mydatabase"]
# mycol = mydb["customers"]
#
# mydoc = mycol.find().sort("name")
#
# for x in mydoc:
#     print(x)
#
# # Insert Multiple Documents, with Specified IDs
# import pymongo
#
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["mydatabase"]
# mycol = mydb["customers"]
#
# mylist = [
#     {"_id": 1, "name": "John", "address": "Highway 37"},
#     {"_id": 2, "name": "Peter", "address": "Lowstreet 27"},
#     {"_id": 3, "name": "Amy", "address": "Apple st 652"},
#     {"_id": 4, "name": "Hannah", "address": "Mountain 21"},
#     {"_id": 5, "name": "Michael", "address": "Valley 345"},
#     {"_id": 6, "name": "Sandy", "address": "Ocean blvd 2"},
#     {"_id": 7, "name": "Betty", "address": "Green Grass 1"},
#     {"_id": 8, "name": "Richard", "address": "Sky st 331"},
#     {"_id": 9, "name": "Susan", "address": "One way 98"}
# ]
#
# x = mycol.insert_many(mylist)
#
# # print list of the _id values of the inserted documents:
#
# print(x.inserted_ids)
#
# # Change the address from "Valley 345" to "Canyon 123":
# import pymongo
#
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["mydatabase"]
# mycol = mydb["customers"]
#
# myquery = {"address": "Valley 345"}
# newvalues = {"$set": {"address": "Canyon 123"}}
#
# mycol.update_one(myquery, newvalues)
#
# # print "customers" after the update:
#
# for x in mycol.find():
#     print(x)
