"""
MongoDB connection setup using Motor (async driver)
"""
from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

# Initialize MongoDB client
client = AsyncIOMotorClient(settings.MONGODB_URI)
database = client[settings.MONGODB_DB_NAME]

def get_database():
    """Returns the MongoDB database instance"""
    return database

def get_collection():
    """Returns the debts collection"""
    return database[settings.MONGODB_COLLECTION]