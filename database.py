# database.py
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    def __init__(self):
        # 🔧 MongoDB connection string - modify as needed
        self.connection_string = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.database_name = os.getenv('DB_NAME', 'recipe_management')
        self.client = None
        self.db = None
    
    def connect(self):
        """🔗 Establish connection to MongoDB"""
        try:
            self.client = MongoClient(self.connection_string)
            # Test the connection
            self.client.admin.command('ping')
            self.db = self.client[self.database_name]
            print("✅ Successfully connected to MongoDB!")
            return True
        except ConnectionFailure as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            return False
    
    def get_collection(self, collection_name):
        """📂 Get a specific collection"""
        if self.db is not None:
            return self.db[collection_name]
        else:
            raise Exception("❌ Database not connected!")
    
    def close_connection(self):
        """🔒 Close database connection"""
        if self.client:
            self.client.close()
            print("🔒 Database connection closed!")

# 🌟 Singleton pattern for database connection
db_connection = DatabaseConnection()