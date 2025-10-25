from datetime import datetime
from typing import Optional, List, Dict, Any
from bson import ObjectId
import uuid
from core.MongoDB.connection import get_collection


class TitleDB:
    """
    Database operations for Title collection
    """
    
    @staticmethod
    def create(title_text: str = "") -> Dict[str, Any]:
        """
        POST: Create a new title
        
        Args:
            title_text (str): Title text
            
        Returns:
            dict: Created title document
        """
        collection = get_collection("Title")
        now = datetime.utcnow()
        
        title_doc = {
            "id_title": str(uuid.uuid4()),
            "title": title_text,
            "create_at": now,
            "last_update": now
        }
        
        result = collection.insert_one(title_doc)
        title_doc["_id"] = str(result.inserted_id)
        
        return title_doc
    
    @staticmethod
    def get_by_id(id_title: str) -> Optional[Dict[str, Any]]:
        """
        GET: Get title by ID
        
        Args:
            id_title (str): Title ID
            
        Returns:
            dict: Title document or None
        """
        collection = get_collection("Title")
        title = collection.find_one({"id_title": id_title})
        
        if title:
            title["_id"] = str(title["_id"])
        
        return title
    
    @staticmethod
    def get_all(limit: int = 100, skip: int = 0) -> List[Dict[str, Any]]:
        """
        GET: Get all titles with pagination
        
        Args:
            limit (int): Number of documents to return
            skip (int): Number of documents to skip
            
        Returns:
            list: List of title documents
        """
        collection = get_collection("Title")
        titles = list(collection.find().sort("last_update", -1).skip(skip).limit(limit))
        
        for title in titles:
            title["_id"] = str(title["_id"])
        
        return titles
    
    @staticmethod
    def update(id_title: str, updates: Dict[str, Any]) -> bool:
        """
        POST: Update title information
        
        Args:
            id_title (str): Title ID
            updates (dict): Fields to update
            
        Returns:
            bool: True if updated successfully
        """
        collection = get_collection("Title")
        
        # Always update last_update timestamp
        updates["last_update"] = datetime.utcnow()
        
        result = collection.update_one(
            {"id_title": id_title},
            {"$set": updates}
        )
        
        return result.modified_count > 0
    
    @staticmethod
    def delete(id_title: str) -> bool:
        """
        DELETE: Delete title by ID
        
        Args:
            id_title (str): Title ID
            
        Returns:
            bool: True if deleted successfully
        """
        collection = get_collection("Title")
        result = collection.delete_one({"id_title": id_title})
        
        # Also delete related chats and contexts
        if result.deleted_count > 0:
            ChatDB.delete_by_title(id_title)
        
        return result.deleted_count > 0


class ChatDB:
    """
    Database operations for Chat collection
    """
    
    @staticmethod
    def create(id_title: str) -> Dict[str, Any]:
        """
        POST: Create a new chat
        
        Args:
            id_title (str): Title ID reference
            
        Returns:
            dict: Created chat document
        """
        collection = get_collection("Chat")
        
        chat_doc = {
            "id_chat": str(uuid.uuid4()),
            "id_title": id_title,
            "create_at": datetime.utcnow()
        }
        
        result = collection.insert_one(chat_doc)
        chat_doc["_id"] = str(result.inserted_id)
        
        # Update title's last_update
        TitleDB.update(id_title, {})
        
        return chat_doc
    
    @staticmethod
    def get_by_id(id_chat: str) -> Optional[Dict[str, Any]]:
        """
        GET: Get chat by ID
        
        Args:
            id_chat (str): Chat ID
            
        Returns:
            dict: Chat document or None
        """
        collection = get_collection("Chat")
        chat = collection.find_one({"id_chat": id_chat})
        
        if chat:
            chat["_id"] = str(chat["_id"])
        
        return chat
    
    @staticmethod
    def get_by_title(id_title: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        GET: Get all chats for a title
        
        Args:
            id_title (str): Title ID
            limit (int): Number of documents to return
            
        Returns:
            list: List of chat documents
        """
        collection = get_collection("Chat")
        chats = list(collection.find({"id_title": id_title}).sort("create_at", -1).limit(limit))
        
        for chat in chats:
            chat["_id"] = str(chat["_id"])
        
        return chats
    
    @staticmethod
    def delete(id_chat: str) -> bool:
        """
        DELETE: Delete chat by ID
        
        Args:
            id_chat (str): Chat ID
            
        Returns:
            bool: True if deleted successfully
        """
        collection = get_collection("Chat")
        result = collection.delete_one({"id_chat": id_chat})
        
        # Also delete related contexts
        if result.deleted_count > 0:
            ContextDB.delete_by_chat(id_chat)
        
        return result.deleted_count > 0
    
    @staticmethod
    def delete_by_title(id_title: str) -> int:
        """
        DELETE: Delete all chats for a title
        
        Args:
            id_title (str): Title ID
            
        Returns:
            int: Number of deleted documents
        """
        collection = get_collection("Chat")
        
        # Get all chat IDs first
        chats = collection.find({"id_title": id_title}, {"id_chat": 1})
        chat_ids = [chat["id_chat"] for chat in chats]
        
        # Delete contexts for all chats
        for chat_id in chat_ids:
            ContextDB.delete_by_chat(chat_id)
        
        # Delete chats
        result = collection.delete_many({"id_title": id_title})
        return result.deleted_count


class ContextDB:
    """
    Database operations for Context collection
    """
    
    @staticmethod
    def create(id_chat: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        POST: Create a new context
        
        Args:
            id_chat (str): Chat ID reference
            context (dict): Context JSON data
            
        Returns:
            dict: Created context document
        """
        collection = get_collection("Context")
        
        context_doc = {
            "id_chat": id_chat,
            "id_context": str(uuid.uuid4()),
            "create_at": datetime.utcnow(),
            "context": context
        }
        
        result = collection.insert_one(context_doc)
        context_doc["_id"] = str(result.inserted_id)
        
        # Update related title's last_update
        chat = ChatDB.get_by_id(id_chat)
        if chat:
            TitleDB.update(chat["id_title"], {})
        
        return context_doc
    
    @staticmethod
    def get_by_id(id_context: str) -> Optional[Dict[str, Any]]:
        """
        GET: Get context by ID
        
        Args:
            id_context (str): Context ID
            
        Returns:
            dict: Context document or None
        """
        collection = get_collection("Context")
        context = collection.find_one({"id_context": id_context})
        
        if context:
            context["_id"] = str(context["_id"])
        
        return context
    
    @staticmethod
    def get_by_chat(id_chat: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        GET: Get all contexts for a chat
        
        Args:
            id_chat (str): Chat ID
            limit (int): Number of documents to return
            
        Returns:
            list: List of context documents
        """
        collection = get_collection("Context")
        contexts = list(collection.find({"id_chat": id_chat}).sort("create_at", 1).limit(limit))
        
        for context in contexts:
            context["_id"] = str(context["_id"])
        
        return contexts
    
    @staticmethod
    def update(id_context: str, context: Dict[str, Any]) -> bool:
        """
        POST: Update context information
        
        Args:
            id_context (str): Context ID
            context (dict): New context data
            
        Returns:
            bool: True if updated successfully
        """
        collection = get_collection("Context")
        
        result = collection.update_one(
            {"id_context": id_context},
            {"$set": {"context": context}}
        )
        
        return result.modified_count > 0
    
    @staticmethod
    def delete(id_context: str) -> bool:
        """
        DELETE: Delete context by ID
        
        Args:
            id_context (str): Context ID
            
        Returns:
            bool: True if deleted successfully
        """
        collection = get_collection("Context")
        result = collection.delete_one({"id_context": id_context})
        
        return result.deleted_count > 0
    
    @staticmethod
    def delete_by_chat(id_chat: str) -> int:
        """
        DELETE: Delete all contexts for a chat
        
        Args:
            id_chat (str): Chat ID
            
        Returns:
            int: Number of deleted documents
        """
        collection = get_collection("Context")
        result = collection.delete_many({"id_chat": id_chat})
        
        return result.deleted_count
