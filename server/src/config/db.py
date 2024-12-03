# src/config/db.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB Configuration
Mongo_URL = os.getenv("MONGO_URL")
Mongo_DB = os.getenv("MONGO_DB")

def connect_to_mongo():
    """Function to connect to MongoDB and return the database object."""
    try:
        client = MongoClient(Mongo_URL)  # Create MongoDB client
        db = client[Mongo_DB]  # Get the database
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None
