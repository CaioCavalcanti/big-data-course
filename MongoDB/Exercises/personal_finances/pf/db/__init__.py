from pymongo import MongoClient

connection = MongoClient('localhost', 27017)
db = connection.pf
