from pymongo.server_api import ServerApi
from motor.motor_asyncio import AsyncIOMotorClient


uri = "mongodb+srv://admin:smk4305a@auth.fqak4d3.mongodb.net/?retryWrites=true&w=majority&appName=AUTH"

client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))

db = client.fastapi_auth
collection = db.users

