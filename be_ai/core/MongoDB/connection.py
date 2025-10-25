import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get MongoDB connection details from environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "AI4SE")


class MongoDBConnection:
    """
    MongoDB Connection Manager
    """
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        """Singleton pattern to ensure only one connection instance"""
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
        return cls._instance

    def connect(self):
        """
        Establish connection to MongoDB
        Returns the database instance
        """
        try:
            if self._client is None:
                self._client = MongoClient(MONGO_URI)
                # Test the connection
                self._client.admin.command('ping')
                print(f"✓ Connected to MongoDB successfully at {MONGO_URI}")
                
            if self._db is None:
                self._db = self._client[DATABASE_NAME]
                print(f"✓ Using database: {DATABASE_NAME}")
                
            return self._db
        
        except ConnectionFailure as e:
            print(f"✗ Failed to connect to MongoDB: {e}")
            raise
        except Exception as e:
            print(f"✗ An error occurred: {e}")
            raise

    def get_database(self):
        """
        Get the database instance
        """
        if self._db is None:
            return self.connect()
        return self._db

    def get_collection(self, collection_name):
        """
        Get a specific collection from the database
        
        Args:
            collection_name (str): Name of the collection
            
        Returns:
            Collection instance
        """
        db = self.get_database()
        return db[collection_name]

    def close(self):
        """
        Close the MongoDB connection
        """
        if self._client is not None:
            self._client.close()
            print("✓ MongoDB connection closed")
            self._client = None
            self._db = None


# Create a global instance
mongo_connection = MongoDBConnection()


def get_db():
    """
    Helper function to get database instance
    """
    return mongo_connection.get_database()


def get_collection(collection_name):
    """
    Helper function to get collection instance
    
    Args:
        collection_name (str): Name of the collection
        
    Returns:
        Collection instance
    """
    return mongo_connection.get_collection(collection_name)
