# API Documentation - Chatbot Learning Assistant

## 🚀 Chạy API Server

```bash
# Khởi động server
python main.py

# Hoặc sử dụng uvicorn trực tiếp
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server sẽ chạy tại: `http://localhost:8000`

API Documentation (Swagger): `http://localhost:8000/docs`

Alternative API docs (ReDoc): `http://localhost:8000/redoc`

---

## 📚 API Endpoints

### **Health Check**
- `GET /api/health` - Kiểm tra trạng thái API và kết nối database

---

## 🏷️ Title Endpoints

### 1. Tạo Title mới
**POST** `/api/titles`

```json
{
  "title": "Học Python cơ bản"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "_id": "...",
    "id_title": "uuid-here",
    "title": "Học Python cơ bản",
    "create_at": "2025-10-25T10:00:00",
    "last_update": "2025-10-25T10:00:00"
  }
}
```

### 2. Lấy Title theo ID
**GET** `/api/titles/{id_title}`

**Response:**
```json
{
  "success": true,
  "data": {
    "id_title": "uuid-here",
    "title": "Học Python cơ bản",
    "create_at": "2025-10-25T10:00:00",
    "last_update": "2025-10-25T10:00:00"
  }
}
```

### 3. Lấy tất cả Titles
**GET** `/api/titles?limit=100&skip=0`

**Response:**
```json
{
  "success": true,
  "data": [...],
  "count": 10
}
```

### 4. Cập nhật Title
**PUT** `/api/titles/{id_title}`

```json
{
  "title": "Học Python nâng cao"
}
```

### 5. Xóa Title
**DELETE** `/api/titles/{id_title}`

⚠️ **Lưu ý**: Xóa title sẽ tự động xóa tất cả chats và contexts liên quan

---

## 💬 Chat Endpoints

### 1. Tạo Chat mới
**POST** `/api/chats`

```json
{
  "id_title": "uuid-of-title"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "_id": "...",
    "id_chat": "uuid-here",
    "id_title": "uuid-of-title",
    "create_at": "2025-10-25T10:00:00"
  }
}
```

### 2. Lấy Chat theo ID
**GET** `/api/chats/{id_chat}`

### 3. Lấy tất cả Chats của một Title
**GET** `/api/titles/{id_title}/chats?limit=100`

**Response:**
```json
{
  "success": true,
  "data": [...],
  "count": 5
}
```

### 4. Xóa Chat
**DELETE** `/api/chats/{id_chat}`

⚠️ **Lưu ý**: Xóa chat sẽ tự động xóa tất cả contexts liên quan

---

## 📝 Context Endpoints

### 1. Tạo Context mới
**POST** `/api/contexts`

```json
{
  "id_chat": "uuid-of-chat",
  "context": {
    "role": "user",
    "message": "Python là gì?",
    "timestamp": "2025-10-25T10:00:00"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "_id": "...",
    "id_context": "uuid-here",
    "id_chat": "uuid-of-chat",
    "create_at": "2025-10-25T10:00:00",
    "context": {
      "role": "user",
      "message": "Python là gì?",
      "timestamp": "2025-10-25T10:00:00"
    }
  }
}
```

### 2. Lấy Context theo ID
**GET** `/api/contexts/{id_context}`

### 3. Lấy tất cả Contexts của một Chat
**GET** `/api/chats/{id_chat}/contexts?limit=100`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id_context": "uuid-1",
      "id_chat": "uuid-of-chat",
      "create_at": "2025-10-25T10:00:00",
      "context": {
        "role": "user",
        "message": "Python là gì?"
      }
    },
    {
      "id_context": "uuid-2",
      "id_chat": "uuid-of-chat",
      "create_at": "2025-10-25T10:00:05",
      "context": {
        "role": "assistant",
        "message": "Python là ngôn ngữ lập trình..."
      }
    }
  ],
  "count": 2
}
```

### 4. Cập nhật Context
**PUT** `/api/contexts/{id_context}`

```json
{
  "context": {
    "role": "user",
    "message": "Updated message",
    "edited": true
  }
}
```

### 5. Xóa Context
**DELETE** `/api/contexts/{id_context}`

---

## 🔧 Ví dụ sử dụng với cURL

### Tạo một cuộc hội thoại hoàn chỉnh:

```bash
# 1. Tạo Title
curl -X POST "http://localhost:8000/api/titles" \
  -H "Content-Type: application/json" \
  -d '{"title": "Học Python"}'

# Response sẽ trả về id_title, lưu lại để dùng

# 2. Tạo Chat
curl -X POST "http://localhost:8000/api/chats" \
  -H "Content-Type: application/json" \
  -d '{"id_title": "YOUR_TITLE_ID"}'

# Response sẽ trả về id_chat, lưu lại để dùng

# 3. Thêm Context (câu hỏi của user)
curl -X POST "http://localhost:8000/api/contexts" \
  -H "Content-Type: application/json" \
  -d '{
    "id_chat": "YOUR_CHAT_ID",
    "context": {
      "role": "user",
      "message": "Python là gì?"
    }
  }'

# 4. Thêm Context (câu trả lời của assistant)
curl -X POST "http://localhost:8000/api/contexts" \
  -H "Content-Type: application/json" \
  -d '{
    "id_chat": "YOUR_CHAT_ID",
    "context": {
      "role": "assistant",
      "message": "Python là ngôn ngữ lập trình bậc cao..."
    }
  }'

# 5. Lấy toàn bộ lịch sử chat
curl -X GET "http://localhost:8000/api/chats/YOUR_CHAT_ID/contexts"
```

---

## 🐍 Ví dụ sử dụng với Python

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Tạo Title
response = requests.post(
    f"{BASE_URL}/api/titles",
    json={"title": "Học Python cơ bản"}
)
title = response.json()["data"]
print(f"Created title: {title['id_title']}")

# 2. Tạo Chat
response = requests.post(
    f"{BASE_URL}/api/chats",
    json={"id_title": title["id_title"]}
)
chat = response.json()["data"]
print(f"Created chat: {chat['id_chat']}")

# 3. Thêm messages
messages = [
    {"role": "user", "message": "Python là gì?"},
    {"role": "assistant", "message": "Python là ngôn ngữ lập trình bậc cao..."},
    {"role": "user", "message": "Làm sao để học Python?"},
    {"role": "assistant", "message": "Bạn có thể bắt đầu với..."}
]

for msg in messages:
    response = requests.post(
        f"{BASE_URL}/api/contexts",
        json={
            "id_chat": chat["id_chat"],
            "context": msg
        }
    )
    print(f"Added context: {msg['role']}")

# 4. Lấy lịch sử chat
response = requests.get(f"{BASE_URL}/api/chats/{chat['id_chat']}/contexts")
contexts = response.json()["data"]

print(f"\nChat history ({len(contexts)} messages):")
for ctx in contexts:
    role = ctx["context"]["role"]
    message = ctx["context"]["message"]
    print(f"{role}: {message}")
```

---

## 📊 Response Format

Tất cả endpoints đều trả về JSON với format:

### Success Response:
```json
{
  "success": true,
  "data": {...},
  "count": 10  // optional, for list endpoints
}
```

### Error Response:
```json
{
  "detail": "Error message here"
}
```

---

## ⚡ Features

- ✅ Tự động khởi tạo database khi start server
- ✅ Schema validation cho tất cả collections
- ✅ Cascade delete (xóa title → xóa chats → xóa contexts)
- ✅ CORS enabled (cho phép frontend kết nối)
- ✅ Swagger UI documentation tự động
- ✅ Error handling đầy đủ
- ✅ Timestamps tự động (create_at, last_update)

---

## 🔗 Workflow điển hình

1. **Tạo Title** → Đại diện cho một chủ đề học tập
2. **Tạo Chat** → Tạo cuộc hội thoại dưới title đó
3. **Thêm Contexts** → Thêm từng câu hỏi/trả lời vào chat
4. **Query** → Lấy lịch sử, cập nhật, hoặc xóa khi cần

**Last update tự động**: Mỗi khi thêm context mới, `last_update` của title sẽ tự động được cập nhật!
