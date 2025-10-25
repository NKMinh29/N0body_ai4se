from datetime import datetime
from core.MongoDB.connection import get_db


def init_collections():
    """
    Initialize all collections with proper schema validation
    """
    db = get_db()
    
    # Title Collection Schema
    title_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["id_title", "create_at", "last_update"],
            "properties": {
                "id_title": {
                    "bsonType": "string",
                    "description": "Unique identifier for the title"
                },
                "create_at": {
                    "bsonType": "date",
                    "description": "Creation date"
                },
                "last_update": {
                    "bsonType": "date",
                    "description": "Last update date"
                },
                "title": {
                    "bsonType": "string",
                    "description": "Title text"
                }
            }
        }
    }
    
    # Chat Collection Schema
    chat_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["id_chat", "id_title", "create_at"],
            "properties": {
                "id_chat": {
                    "bsonType": "string",
                    "description": "Unique identifier for the chat"
                },
                "id_title": {
                    "bsonType": "string",
                    "description": "Reference to title ID"
                },
                "create_at": {
                    "bsonType": "date",
                    "description": "Creation date"
                }
            }
        }
    }
    
    # Context Collection Schema
    context_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["id_chat", "id_context", "create_at", "context"],
            "properties": {
                "id_chat": {
                    "bsonType": "string",
                    "description": "Reference to chat ID"
                },
                "id_context": {
                    "bsonType": "string",
                    "description": "Unique identifier for the context"
                },
                "create_at": {
                    "bsonType": "date",
                    "description": "Creation date"
                },
                "context": {
                    "bsonType": "object",
                    "description": "JSON object containing chat context"
                }
            }
        }
    }
    
    # Create collections with validation
    collections = {
        "Title": title_validator,
        "Chat": chat_validator,
        "Context": context_validator
    }
    
    for collection_name, validator in collections.items():
        try:
            # Check if collection exists
            if collection_name in db.list_collection_names():
                print(f"✓ Collection '{collection_name}' already exists")
            else:
                # Create collection with validation
                db.create_collection(collection_name, validator=validator)
                print(f"✓ Created collection '{collection_name}'")
                
            # Create indexes
            if collection_name == "Title":
                db[collection_name].create_index("id_title", unique=True)
                db[collection_name].create_index("last_update")
                print(f"  - Created indexes for '{collection_name}'")
                
            elif collection_name == "Chat":
                db[collection_name].create_index("id_chat", unique=True)
                db[collection_name].create_index("id_title")
                db[collection_name].create_index("create_at")
                print(f"  - Created indexes for '{collection_name}'")
                
            elif collection_name == "Context":
                db[collection_name].create_index([("id_chat", 1), ("id_context", 1)], unique=True)
                db[collection_name].create_index("id_chat")
                db[collection_name].create_index("create_at")
                print(f"  - Created indexes for '{collection_name}'")
                
        except Exception as e:
            print(f"✗ Error creating collection '{collection_name}': {e}")
    
    print("\n✓ Database initialization completed!")


if __name__ == "__main__":
    init_collections()
