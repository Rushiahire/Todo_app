from pymongo import MongoClient

mango_url = 'localhost:27017'
client = MongoClient(mango_url)

database_name = 'todo'
database = client[database_name]
