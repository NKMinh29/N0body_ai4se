"""
Main entry point for the Chatbot Learning Assistant API
Run with: python main.py or uvicorn main:app --reload
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

from core.MongoDB import init_collections
import core.api as api_functions


# Initialize FastAPI app
app = FastAPI(
    title="Chatbot Learning Assistant API",
    description="API for chatbot learning assistant with MongoDB",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response
class TitleCreate(BaseModel):
    title: str = Field(..., description="Title text")


class TitleUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Title text to update")


class ChatCreate(BaseModel):
    id_title: str = Field(..., description="Title ID reference")


class ContextCreate(BaseModel):
    id_chat: str = Field(..., description="Chat ID reference")
    context: Dict[str, Any] = Field(..., description="Context JSON data")


class ContextUpdate(BaseModel):
    context: Dict[str, Any] = Field(..., description="New context data")


# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database collections on startup"""
    try:
        init_collections()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Error initializing database: {e}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Chatbot Learning Assistant API",
        "version": "1.0.0",
        "docs": "/docs"
    }


# ==================== TITLE ENDPOINTS ====================

@app.post("/api/titles", response_model=dict, tags=["Titles"])
async def create_title_endpoint(title_data: TitleCreate):
    """Create a new title"""
    return api_functions.create_title(title_data.title)


@app.get("/api/titles/{id_title}", response_model=dict, tags=["Titles"])
async def get_title_endpoint(id_title: str):
    """Get title by ID"""
    return api_functions.get_title_by_id(id_title)


@app.get("/api/titles", response_model=dict, tags=["Titles"])
async def get_all_titles_endpoint(
    limit: int = Query(100, description="Number of titles to return"),
    skip: int = Query(0, description="Number of titles to skip")
):
    """Get all titles with pagination"""
    return api_functions.get_all_titles(limit, skip)


@app.put("/api/titles/{id_title}", response_model=dict, tags=["Titles"])
async def update_title_endpoint(id_title: str, title_data: TitleUpdate):
    """Update title information"""
    return api_functions.update_title(id_title, title_data.title)


@app.delete("/api/titles/{id_title}", response_model=dict, tags=["Titles"])
async def delete_title_endpoint(id_title: str):
    """Delete title by ID (cascades to chats and contexts)"""
    return api_functions.delete_title(id_title)


# ==================== CHAT ENDPOINTS ====================

@app.post("/api/chats", response_model=dict, tags=["Chats"])
async def create_chat_endpoint(chat_data: ChatCreate):
    """Create a new chat"""
    return api_functions.create_chat(chat_data.id_title)


@app.get("/api/chats/{id_chat}", response_model=dict, tags=["Chats"])
async def get_chat_endpoint(id_chat: str):
    """Get chat by ID"""
    return api_functions.get_chat_by_id(id_chat)


@app.get("/api/titles/{id_title}/chats", response_model=dict, tags=["Chats"])
async def get_chats_by_title_endpoint(
    id_title: str,
    limit: int = Query(100, description="Number of chats to return")
):
    """Get all chats for a title"""
    return api_functions.get_chats_by_title(id_title, limit)


@app.delete("/api/chats/{id_chat}", response_model=dict, tags=["Chats"])
async def delete_chat_endpoint(id_chat: str):
    """Delete chat by ID (cascades to contexts)"""
    return api_functions.delete_chat(id_chat)


# ==================== CONTEXT ENDPOINTS ====================

@app.post("/api/contexts", response_model=dict, tags=["Contexts"])
async def create_context_endpoint(context_data: ContextCreate):
    """Create a new context"""
    return api_functions.create_context(context_data.id_chat, context_data.context)


@app.get("/api/contexts/{id_context}", response_model=dict, tags=["Contexts"])
async def get_context_endpoint(id_context: str):
    """Get context by ID"""
    return api_functions.get_context_by_id(id_context)


@app.get("/api/chats/{id_chat}/contexts", response_model=dict, tags=["Contexts"])
async def get_contexts_by_chat_endpoint(
    id_chat: str,
    limit: int = Query(100, description="Number of contexts to return")
):
    """Get all contexts for a chat"""
    return api_functions.get_contexts_by_chat(id_chat, limit)


@app.put("/api/contexts/{id_context}", response_model=dict, tags=["Contexts"])
async def update_context_endpoint(id_context: str, context_data: ContextUpdate):
    """Update context information"""
    return api_functions.update_context(id_context, context_data.context)


@app.delete("/api/contexts/{id_context}", response_model=dict, tags=["Contexts"])
async def delete_context_endpoint(id_context: str):
    """Delete context by ID"""
    return api_functions.delete_context(id_context)


# ==================== HEALTH CHECK ====================

@app.get("/api/health", tags=["Health"])
async def health_check_endpoint():
    """Health check endpoint"""
    return api_functions.check_health()


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Chatbot Learning Assistant API...")
    print("📖 Documentation: http://localhost:8000/docs")
    print("🔗 API URL: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
