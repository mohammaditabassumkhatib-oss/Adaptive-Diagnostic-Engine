# app/db/connection.py

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

client = None

def get_client() -> AsyncIOMotorClient:
    global client
    if client is None:
        uri = os.getenv("MONGODB_URI")
        print(f"DEBUG - MONGODB_URI: {uri}")   # ← add this line
        client = AsyncIOMotorClient(uri)
    return client

def get_database():
    return get_client()[os.getenv("DB_NAME", "adaptive_db")]
