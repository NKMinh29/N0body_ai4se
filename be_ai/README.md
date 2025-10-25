# Chatbot Learning Assistant API 🤖

Hệ thống API RESTful cho trợ lý chatbot học tập, sử dụng FastAPI và MongoDB.

## 🎯 Tính năng

- ✅ RESTful API với FastAPI
- ✅ MongoDB để lưu trữ dữ liệu
- ✅ CRUD operations đầy đủ cho Title, Chat, Context
- ✅ Cascade delete (xóa tự động dữ liệu liên quan)
- ✅ Automatic timestamps (create_at, last_update)
- ✅ Schema validation
- ✅ API Documentation tự động (Swagger UI)
- ✅ CORS enabled
- ✅ Health check endpoint

## 📁 Cấu trúc dự án

```
Ai4SE/
├── main.py                    # FastAPI application
├── example_usage.py           # Demo MongoDB operations
├── test_api.py               # API test suite
├── API_DOCS.md               # Detailed API documentation
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── docker-compose.yml        # Docker compose config
└── core/
    ├── AIssistance.py
    ├── OCR.py
    └── MongoDB/
        ├── __init__.py
        ├── connection.py     # MongoDB connection manager
        ├── db.py            # Database operations (CRUD)
        └── init_collection.py # Database initialization
```

## 🚀 Cài đặt

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 2. Cấu hình môi trường

Tạo file `.env`:

```env
MONGO_URI=mongodb://localhost:27017/
DATABASE_NAME=AI4SE
```

### 3. Khởi động MongoDB

Sử dụng Docker:
```bash
docker-compose up -d
```

Hoặc cài đặt MongoDB trực tiếp trên máy.

### 4. Khởi động API Server

```bash
python main.py
```

Server sẽ chạy tại: `http://localhost:8000`

## 📚 API Documentation

### Swagger UI (Interactive)
Truy cập: `http://localhost:8000/docs`

### ReDoc
Truy cập: `http://localhost:8000/redoc`

### Chi tiết API
Xem file [API_DOCS.md](API_DOCS.md)

## 🧪 Testing

### Test tất cả endpoints:

```bash
python test_api.py
```

### Test MongoDB operations:

```bash
python example_usage.py
```

## 📖 Sử dụng cơ bản

### 1. Tạo một cuộc hội thoại

```python
import requests

BASE_URL = "http://localhost:8000"

# Tạo title
title = requests.post(
    f"{BASE_URL}/api/titles",
    json={"title": "Học Python"}
).json()["data"]

# Tạo chat
chat = requests.post(
    f"{BASE_URL}/api/chats",
    json={"id_title": title["id_title"]}
).json()["data"]

# Thêm message
context = requests.post(
    f"{BASE_URL}/api/contexts",
    json={
        "id_chat": chat["id_chat"],
        "context": {
            "role": "user",
            "message": "Python là gì?"
        }
    }
).json()["data"]
```

### 2. Lấy lịch sử chat

```python
# Lấy tất cả contexts của một chat
response = requests.get(
    f"{BASE_URL}/api/chats/{chat['id_chat']}/contexts"
)
contexts = response.json()["data"]

for ctx in contexts:
    print(f"{ctx['context']['role']}: {ctx['context']['message']}")
```

## 🗄️ Database Schema

### Title Collection
```json
{
  "id_title": "uuid",
  "title": "string",
  "create_at": "datetime",
  "last_update": "datetime"
}
```

### Chat Collection
```json
{
  "id_chat": "uuid",
  "id_title": "uuid (reference)",
  "create_at": "datetime"
}
```

### Context Collection
```json
{
  "id_chat": "uuid (reference)",
  "id_context": "uuid",
  "create_at": "datetime",
  "context": {
    "role": "string",
    "message": "string",
    // ... any other fields
  }
}
```

## 🔗 API Endpoints

### Title
- `POST /api/titles` - Tạo title mới
- `GET /api/titles/{id_title}` - Lấy title theo ID
- `GET /api/titles` - Lấy tất cả titles
- `PUT /api/titles/{id_title}` - Cập nhật title
- `DELETE /api/titles/{id_title}` - Xóa title

### Chat
- `POST /api/chats` - Tạo chat mới
- `GET /api/chats/{id_chat}` - Lấy chat theo ID
- `GET /api/titles/{id_title}/chats` - Lấy tất cả chats của title
- `DELETE /api/chats/{id_chat}` - Xóa chat

### Context
- `POST /api/contexts` - Tạo context mới
- `GET /api/contexts/{id_context}` - Lấy context theo ID
- `GET /api/chats/{id_chat}/contexts` - Lấy tất cả contexts của chat
- `PUT /api/contexts/{id_context}` - Cập nhật context
- `DELETE /api/contexts/{id_context}` - Xóa context

### Health
- `GET /api/health` - Kiểm tra trạng thái API

## 🛠️ Technologies

- **FastAPI** - Modern web framework
- **MongoDB** - NoSQL database
- **PyMongo** - MongoDB driver
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## 💡 Tips

1. **Cascade Delete**: Xóa title sẽ tự động xóa tất cả chats và contexts liên quan
2. **Auto Update**: Thêm context mới sẽ tự động cập nhật `last_update` của title
3. **Validation**: Tất cả collections đều có schema validation
4. **Indexes**: Đã tạo indexes để tối ưu truy vấn

## 🤝 Contributing

Mọi đóng góp đều được chào đón!

## 📝 License

MIT License

---

Made with ❤️ for learning
