"""
API Helper Functions for Chatbot Learning Assistant
Contains business logic separated from FastAPI endpoints
"""

from typing import Optional, Dict, Any, List
from fastapi import HTTPException

from core.MongoDB import TitleDB, ChatDB, ContextDB


# ==================== TITLE FUNCTIONS ====================

def create_title(title_text: str) -> Dict[str, Any]:
    """
    Create a new title
    
    Args:
        title_text: Title text
        
    Returns:
        Created title document
        
    Raises:
        HTTPException: If creation fails
    """
    try:
        title = TitleDB.create(title_text=title_text)
        return {"success": True, "data": title}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_title_by_id(id_title: str) -> Dict[str, Any]:
    """
    Get title by ID
    
    Args:
        id_title: Title ID
        
    Returns:
        Title document
        
    Raises:
        HTTPException: If title not found
    """
    title = TitleDB.get_by_id(id_title)
    if not title:
        raise HTTPException(status_code=404, detail="Title not found")
    return {"success": True, "data": title}


def get_all_titles(limit: int = 100, skip: int = 0) -> Dict[str, Any]:
    """
    Get all titles with pagination
    
    Args:
        limit: Number of titles to return
        skip: Number of titles to skip
        
    Returns:
        List of titles
        
    Raises:
        HTTPException: If query fails
    """
    try:
        titles = TitleDB.get_all(limit=limit, skip=skip)
        return {"success": True, "data": titles, "count": len(titles)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def update_title(id_title: str, title_text: Optional[str] = None) -> Dict[str, Any]:
    """
    Update title information
    
    Args:
        id_title: Title ID
        title_text: New title text
        
    Returns:
        Updated title document
        
    Raises:
        HTTPException: If title not found or update fails
    """
    # Check if title exists
    if not TitleDB.get_by_id(id_title):
        raise HTTPException(status_code=404, detail="Title not found")
    
    # Prepare updates
    updates = {}
    if title_text is not None:
        updates["title"] = title_text
    
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    try:
        success = TitleDB.update(id_title, updates)
        if success:
            updated_title = TitleDB.get_by_id(id_title)
            return {"success": True, "data": updated_title}
        else:
            raise HTTPException(status_code=500, detail="Update failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_title(id_title: str) -> Dict[str, Any]:
    """
    Delete title by ID (cascades to chats and contexts)
    
    Args:
        id_title: Title ID
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If title not found or delete fails
    """
    if not TitleDB.get_by_id(id_title):
        raise HTTPException(status_code=404, detail="Title not found")
    
    try:
        success = TitleDB.delete(id_title)
        if success:
            return {"success": True, "message": "Title deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Delete failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== CHAT FUNCTIONS ====================

def create_chat(id_title: str) -> Dict[str, Any]:
    """
    Create a new chat
    
    Args:
        id_title: Title ID reference
        
    Returns:
        Created chat document
        
    Raises:
        HTTPException: If title not found or creation fails
    """
    # Verify title exists
    if not TitleDB.get_by_id(id_title):
        raise HTTPException(status_code=404, detail="Title not found")
    
    try:
        chat = ChatDB.create(id_title=id_title)
        return {"success": True, "data": chat}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_chat_by_id(id_chat: str) -> Dict[str, Any]:
    """
    Get chat by ID
    
    Args:
        id_chat: Chat ID
        
    Returns:
        Chat document
        
    Raises:
        HTTPException: If chat not found
    """
    chat = ChatDB.get_by_id(id_chat)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"success": True, "data": chat}


def get_chats_by_title(id_title: str, limit: int = 100) -> Dict[str, Any]:
    """
    Get all chats for a title
    
    Args:
        id_title: Title ID
        limit: Number of chats to return
        
    Returns:
        List of chats
        
    Raises:
        HTTPException: If title not found or query fails
    """
    # Verify title exists
    if not TitleDB.get_by_id(id_title):
        raise HTTPException(status_code=404, detail="Title not found")
    
    try:
        chats = ChatDB.get_by_title(id_title, limit=limit)
        return {"success": True, "data": chats, "count": len(chats)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_chat(id_chat: str) -> Dict[str, Any]:
    """
    Delete chat by ID (cascades to contexts)
    
    Args:
        id_chat: Chat ID
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If chat not found or delete fails
    """
    if not ChatDB.get_by_id(id_chat):
        raise HTTPException(status_code=404, detail="Chat not found")
    
    try:
        success = ChatDB.delete(id_chat)
        if success:
            return {"success": True, "message": "Chat deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Delete failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== CONTEXT FUNCTIONS ====================

def create_context(id_chat: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new context
    
    Args:
        id_chat: Chat ID reference
        context: Context JSON data
        
    Returns:
        Created context document
        
    Raises:
        HTTPException: If chat not found or creation fails
    """
    # Verify chat exists
    if not ChatDB.get_by_id(id_chat):
        raise HTTPException(status_code=404, detail="Chat not found")
    
    try:
        context_doc = ContextDB.create(id_chat=id_chat, context=context)
        return {"success": True, "data": context_doc}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_context_by_id(id_context: str) -> Dict[str, Any]:
    """
    Get context by ID
    
    Args:
        id_context: Context ID
        
    Returns:
        Context document
        
    Raises:
        HTTPException: If context not found
    """
    context = ContextDB.get_by_id(id_context)
    if not context:
        raise HTTPException(status_code=404, detail="Context not found")
    return {"success": True, "data": context}


def get_contexts_by_chat(id_chat: str, limit: int = 100) -> Dict[str, Any]:
    """
    Get all contexts for a chat
    
    Args:
        id_chat: Chat ID
        limit: Number of contexts to return
        
    Returns:
        List of contexts
        
    Raises:
        HTTPException: If chat not found or query fails
    """
    # Verify chat exists
    if not ChatDB.get_by_id(id_chat):
        raise HTTPException(status_code=404, detail="Chat not found")
    
    try:
        contexts = ContextDB.get_by_chat(id_chat, limit=limit)
        return {"success": True, "data": contexts, "count": len(contexts)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def update_context(id_context: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update context information
    
    Args:
        id_context: Context ID
        context: New context data
        
    Returns:
        Updated context document
        
    Raises:
        HTTPException: If context not found or update fails
    """
    # Check if context exists
    if not ContextDB.get_by_id(id_context):
        raise HTTPException(status_code=404, detail="Context not found")
    
    try:
        success = ContextDB.update(id_context, context)
        if success:
            updated_context = ContextDB.get_by_id(id_context)
            return {"success": True, "data": updated_context}
        else:
            raise HTTPException(status_code=500, detail="Update failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def delete_context(id_context: str) -> Dict[str, Any]:
    """
    Delete context by ID
    
    Args:
        id_context: Context ID
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If context not found or delete fails
    """
    if not ContextDB.get_by_id(id_context):
        raise HTTPException(status_code=404, detail="Context not found")
    
    try:
        success = ContextDB.delete(id_context)
        if success:
            return {"success": True, "message": "Context deleted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Delete failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== HEALTH CHECK ====================

def check_health() -> Dict[str, Any]:
    """
    Check API and database health
    
    Returns:
        Health status
    """
    try:
        from datetime import datetime
        from core.MongoDB.connection import mongo_connection
        
        db = mongo_connection.get_database()
        # Test connection
        db.client.admin.command('ping')
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        from datetime import datetime
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

