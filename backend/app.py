from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import datetime
from typing import List, Dict
import uuid
from gemini_service import gemini_service

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Simulated chat database
chat_database = {
    "conversations": [
        {
            "id": "conv_001",
            "title": "Unclear Input, Seeking Assistance",
            "lastMessage": "Could you please clarify what you're looking for?",
            "timestamp": "2024-10-25T10:30:00Z",
            "messageCount": 5
        },
        {
            "id": "conv_002", 
            "title": "Hướng dẫn cài Node.js và MongoDB",
            "lastMessage": "Để cài đặt Node.js và MongoDB, bạn cần làm theo các bước sau...",
            "timestamp": "2024-10-25T09:15:00Z",
            "messageCount": 8
        },
        {
            "id": "conv_003",
            "title": "Hướng dẫn thiết kế mạch đếm 00-99",
            "lastMessage": "Mạch đếm 00-99 sử dụng 2 IC 74LS90 và các cổng logic...",
            "timestamp": "2024-10-25T08:45:00Z",
            "messageCount": 12
        },
        {
            "id": "conv_004",
            "title": "Synchronous Parallel Data Load",
            "lastMessage": "Synchronous parallel loading improves performance by...",
            "timestamp": "2024-10-24T16:20:00Z",
            "messageCount": 6
        },
        {
            "id": "conv_005",
            "title": "So Sánh Thanh Ghi Dịch IO",
            "lastMessage": "Thanh ghi dịch IO có các đặc điểm khác nhau về tốc độ...",
            "timestamp": "2024-10-24T14:30:00Z",
            "messageCount": 9
        },
        {
            "id": "conv_006",
            "title": "Hàm Lambda trong C++",
            "lastMessage": "Lambda functions trong C++ cho phép bạn viết code ngắn gọn...",
            "timestamp": "2024-10-24T11:15:00Z",
            "messageCount": 7
        },
        {
            "id": "conv_007",
            "title": "Cập nhật One Piece: God Valley",
            "lastMessage": "Trong chapter mới nhất, chúng ta thấy được bí mật của God Valley...",
            "timestamp": "2024-10-23T20:00:00Z",
            "messageCount": 15
        },
        {
            "id": "conv_008",
            "title": "Hướng dẫn phân loại táo bằng Computer Vision",
            "lastMessage": "Sử dụng OpenCV và machine learning để phân loại táo...",
            "timestamp": "2024-10-23T15:30:00Z",
            "messageCount": 11
        },
        {
            "id": "conv_009",
            "title": "Giải thích Bảng Trạng Thái Thanh Ghi",
            "lastMessage": "Bảng trạng thái mô tả hoạt động của thanh ghi dịch...",
            "timestamp": "2024-10-22T13:45:00Z",
            "messageCount": 4
        },
        {
            "id": "conv_010",
            "title": "Phân tích thống kê điểm số nhóm",
            "lastMessage": "Dựa trên dữ liệu điểm số, nhóm có điểm trung bình 8.5...",
            "timestamp": "2024-10-22T10:20:00Z",
            "messageCount": 6
        },
        {
            "id": "conv_011",
            "title": "Idea mini game khởi động họp clb",
            "lastMessage": "Đề xuất một số mini game để khởi động buổi họp CLB...",
            "timestamp": "2024-10-21T18:00:00Z",
            "messageCount": 8
        },
        {
            "id": "conv_012",
            "title": "Flip-Flop Lab: Divide-by-4 Counter",
            "lastMessage": "Thí nghiệm Flip-Flop để tạo bộ đếm chia 4...",
            "timestamp": "2024-10-21T14:15:00Z",
            "messageCount": 10
        }
    ],
    "messages": {
        "conv_001": [
            {"id": "msg_001_1", "content": "I need help with something but I'm not sure how to explain it", "sender": "user", "timestamp": "2024-10-25T10:25:00Z"},
            {"id": "msg_001_2", "content": "I'd be happy to help! Could you provide more details about what you're trying to accomplish?", "sender": "assistant", "timestamp": "2024-10-25T10:26:00Z"},
            {"id": "msg_001_3", "content": "It's related to programming but I don't know the exact terms", "sender": "user", "timestamp": "2024-10-25T10:28:00Z"},
            {"id": "msg_001_4", "content": "No problem! You can describe it in your own words, and I'll help you figure out the technical details.", "sender": "assistant", "timestamp": "2024-10-25T10:29:00Z"},
            {"id": "msg_001_5", "content": "Could you please clarify what you're looking for?", "sender": "assistant", "timestamp": "2024-10-25T10:30:00Z"}
        ],
        "conv_002": [
            {"id": "msg_002_1", "content": "Làm sao để cài đặt Node.js và MongoDB trên máy tính?", "sender": "user", "timestamp": "2024-10-25T09:10:00Z"},
            {"id": "msg_002_2", "content": "Để cài đặt Node.js và MongoDB, bạn có thể làm theo các bước sau:", "sender": "assistant", "timestamp": "2024-10-25T09:11:00Z"},
            {"id": "msg_002_3", "content": "1. Tải Node.js từ trang chủ nodejs.org", "sender": "assistant", "timestamp": "2024-10-25T09:12:00Z"},
            {"id": "msg_002_4", "content": "2. Cài đặt MongoDB Community Edition", "sender": "assistant", "timestamp": "2024-10-25T09:13:00Z"},
            {"id": "msg_002_5", "content": "Có cách nào cài đặt nhanh hơn không?", "sender": "user", "timestamp": "2024-10-25T09:14:00Z"},
            {"id": "msg_002_6", "content": "Bạn có thể sử dụng package manager như Homebrew (macOS) hoặc Chocolatey (Windows)", "sender": "assistant", "timestamp": "2024-10-25T09:15:00Z"},
            {"id": "msg_002_7", "content": "Để cài đặt Node.js và MongoDB, bạn cần làm theo các bước sau...", "sender": "assistant", "timestamp": "2024-10-25T09:15:00Z"}
        ]
    }
}

@app.route('/api/conversations', methods=['GET'])
def get_conversations():
    """Get all conversations"""
    return jsonify({
        "conversations": chat_database["conversations"],
        "status": "success"
    })

@app.route('/api/messages', methods=['GET'])
def get_messages():
    """Get messages for a specific conversation"""
    conversation_id = request.args.get('conversationId')
    
    if not conversation_id:
        return jsonify({"error": "conversationId is required"}), 400
    
    messages = chat_database["messages"].get(conversation_id, [])
    
    return jsonify({
        "messages": messages,
        "conversationId": conversation_id,
        "status": "success"
    })

@app.route('/api/messages', methods=['POST'])
def create_message():
    """Create a new message"""
    data = request.get_json()
    
    if not data or not data.get('content') or not data.get('sender'):
        return jsonify({"error": "content and sender are required"}), 400
    
    conversation_id = data.get('conversationId', str(uuid.uuid4()))
    
    # Generate new message
    new_message = {
        "id": f"msg_{conversation_id}_{len(chat_database['messages'].get(conversation_id, [])) + 1}",
        "content": data['content'],
        "sender": data['sender'],
        "timestamp": datetime.datetime.now().isoformat() + "Z"
    }
    
    # Add to database
    if conversation_id not in chat_database["messages"]:
        chat_database["messages"][conversation_id] = []
    
    chat_database["messages"][conversation_id].append(new_message)
    
    # Check if this is a new conversation
    conversation_exists = any(conv["id"] == conversation_id for conv in chat_database["conversations"])
    
    if not conversation_exists:
        # Create new conversation
        new_conversation = {
            "id": conversation_id,
            "title": data['content'][:50] + "..." if len(data['content']) > 50 else data['content'],
            "lastMessage": data['content'],
            "timestamp": new_message["timestamp"],
            "messageCount": 1
        }
        chat_database["conversations"].insert(0, new_conversation)  # Add to beginning
    else:
        # Update existing conversation
        for conv in chat_database["conversations"]:
            if conv["id"] == conversation_id:
                conv["lastMessage"] = data['content']
                conv["timestamp"] = new_message["timestamp"]
                conv["messageCount"] += 1
                break
    
    return jsonify({
        "message": new_message,
        "conversationId": conversation_id,
        "status": "success"
    }), 201

@app.route('/api/conversation/<conversation_id>', methods=['GET'])
def get_conversation_details(conversation_id):
    """Get detailed information about a specific conversation"""
    conversation = None
    for conv in chat_database["conversations"]:
        if conv["id"] == conversation_id:
            conversation = conv
            break
    
    if not conversation:
        return jsonify({"error": "Conversation not found"}), 404
    
    messages = chat_database["messages"].get(conversation_id, [])
    
    return jsonify({
        "conversation": conversation,
        "messages": messages,
        "status": "success"
    })

@app.route('/api/ai-response', methods=['POST'])
def get_ai_response():
    """Get AI response from Gemini based on mode and conversation history"""
    data = request.get_json()
    
    if not data or not data.get('message') or not data.get('mode'):
        return jsonify({"error": "message and mode are required"}), 400
    
    user_message = data['message']
    mode = data['mode']
    conversation_id = data.get('conversationId')
    
    try:
        # Get conversation history if conversation_id is provided
        conversation_history = []
        if conversation_id and conversation_id in chat_database["messages"]:
            conversation_history = chat_database["messages"][conversation_id]
        
        # Get AI response from Gemini
        ai_response = gemini_service.get_response(
            user_message=user_message,
            mode=mode,
            conversation_history=conversation_history
        )
        
        return jsonify({
            "response": ai_response,
            "mode": mode,
            "status": "success"
        })
        
    except Exception as e:
        print(f"Error getting AI response: {str(e)}")
        return jsonify({
            "error": "Failed to get AI response",
            "status": "error"
        }), 500

@app.route('/api/test-gemini', methods=['GET'])
def test_gemini():
    """Test all Gemini API keys"""
    results = {}
    
    for mode in ['math', 'english', 'history', 'general']:
        results[mode] = gemini_service.test_api_key(mode)
    
    return jsonify({
        "api_tests": results,
        "status": "success"
    })

@app.route('/api/search', methods=['GET'])
def search_messages():
    """Search for messages containing the query"""
    query = request.args.get('q', '').strip().lower()
    
    if not query:
        return jsonify({"results": [], "status": "success"})
    
    results = []
    
    # Search through all messages
    for conversation_id, messages in chat_database["messages"].items():
        # Find conversation title
        conversation_title = "Unknown Conversation"
        for conv in chat_database["conversations"]:
            if conv["id"] == conversation_id:
                conversation_title = conv["title"]
                break
        
        # Search messages in this conversation
        for message in messages:
            if query in message["content"].lower():
                results.append({
                    "conversationId": conversation_id,
                    "conversationTitle": conversation_title,
                    "messageId": message["id"],
                    "content": message["content"],
                    "sender": message["sender"],
                    "timestamp": message["timestamp"]
                })
    
    # Sort by timestamp (most recent first)
    results.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return jsonify({
        "results": results,
        "query": query,
        "total": len(results),
        "status": "success"
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "total_conversations": len(chat_database["conversations"]),
        "total_messages": sum(len(msgs) for msgs in chat_database["messages"].values())
    })

if __name__ == '__main__':
    print("🚀 Starting Python Flask Backend Server...")
    print("📊 Simulated Database:")
    print(f"   - {len(chat_database['conversations'])} conversations")
    print(f"   - {sum(len(msgs) for msgs in chat_database['messages'].values())} total messages")
    print("🌐 Server will run on: http://localhost:5001")
    print("📡 API Endpoints:")
    print("   - GET  /api/conversations")
    print("   - GET  /api/messages?conversationId=<id>")
    print("   - POST /api/messages")
    print("   - GET  /api/conversation/<id>")
    print("   - GET  /api/health")
    
    app.run(debug=True, port=5001, host='0.0.0.0')
