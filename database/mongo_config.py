from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


uri = "mongodb+srv://admin:smk4305a@auth.fqak4d3.mongodb.net/?retryWrites=true&w=majority&appName=AUTH"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client.fastapi_auth
collection = db.users

