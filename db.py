from pymongo import MongoClient
import os

# Replace with your own URI or use MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)

db = client["task_management"]
tasks_collection = db["tasks"]
users_collection = db["users"]
