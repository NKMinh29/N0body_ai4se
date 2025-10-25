# Gemini Chat Application with Python Backend

A full-stack chat application that simulates the Gemini interface with a Python Flask backend and Next.js frontend.

## 🚀 Features

- **Real-time Chat Interface**: Modern UI similar to Gemini chat
- **Python Flask Backend**: Simulated chat history with 12 pre-loaded conversations
- **Conversation Management**: Click on previous chats to load their history
- **Message Persistence**: All messages saved to simulated database
- **Responsive Design**: Works on desktop and mobile devices

## 📊 Simulated Data

The backend includes 12 pre-loaded conversations with realistic Vietnamese and English content:

1. "Unclear Input, Seeking Assistance"
2. "Hướng dẫn cài Node.js và MongoDB"
3. "Hướng dẫn thiết kế mạch đếm 00-99"
4. "Synchronous Parallel Data Load"
5. "So Sánh Thanh Ghi Dịch IO"
6. "Hàm Lambda trong C++"
7. "Cập nhật One Piece: God Valley"
8. "Hướng dẫn phân loại táo bằng Computer Vision"
9. "Giải thích Bảng Trạng Thái Thanh Ghi"
10. "Phân tích thống kê điểm số nhóm"
11. "Idea mini game khởi động họp clb"
12. "Flip-Flop Lab: Divide-by-4 Counter"

## 🛠️ Tech Stack

### Frontend
- **Next.js 16** with App Router
- **React 19** with TypeScript
- **Tailwind CSS 4** for styling
- **Client-side components** with state management

### Backend
- **Python 3** with Flask
- **Flask-CORS** for cross-origin requests
- **Simulated database** with in-memory storage
- **RESTful API** endpoints

## 🚀 Quick Start

### Option 1: Automated Start (Recommended)
```bash
# Make the script executable and run
chmod +x start.sh
./start.sh
```

### Option 2: Manual Start

1. **Start Python Backend:**
   ```bash
   cd backend
   pip3 install -r requirements.txt
   python3 app.py
   ```

2. **Start Next.js Frontend:**
   ```bash
   npm install
   npm run dev
   ```

## 🌐 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5001

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/conversations` | Get all conversations |
| GET | `/api/conversation/<id>` | Get specific conversation with messages |
| GET | `/api/messages?conversationId=<id>` | Get messages for conversation |
| POST | `/api/messages` | Create new message |

## 🎯 How It Works

1. **Frontend loads** and fetches conversation list from Python backend
2. **User clicks** on a conversation in the sidebar
3. **Frontend requests** conversation details and messages from backend
4. **Backend responds** with conversation data and message history
5. **Frontend displays** the conversation with full message history
6. **New messages** are sent to backend and stored in simulated database

## 🔧 Configuration

The Python backend runs on port **5001** (to avoid conflicts with macOS AirTunes on port 5000).

To change the port, update:
- `backend/app.py` - Change the port in `app.run()`
- Frontend components - Update API URLs to match new port

## 📁 Project Structure

```
my-app/
├── app/                    # Next.js frontend
│   ├── components/         # React components
│   │   ├── ChatInterface.tsx
│   │   ├── Sidebar.tsx
│   │   ├── ChatArea.tsx
│   │   ├── Header.tsx
│   │   └── FloatingButton.tsx
│   └── page.tsx           # Main page
├── backend/               # Python Flask backend
│   ├── app.py            # Main Flask application
│   └── requirements.txt  # Python dependencies
├── start.sh              # Startup script
└── package.json          # Node.js dependencies
```

## 🎨 UI Features

- **Dark Theme**: Modern dark interface
- **Sidebar Navigation**: Toggle sidebar, conversation list
- **Message Bubbles**: User (blue) and assistant (gray) messages
- **Loading States**: Spinners and loading indicators
- **Responsive Design**: Adapts to different screen sizes
- **Vietnamese Support**: Full Vietnamese text support

## 🧪 Testing

Test the API endpoints:

```bash
# Health check
curl http://localhost:5001/api/health

# Get conversations
curl http://localhost:5001/api/conversations

# Get specific conversation
curl http://localhost:5001/api/conversation/conv_001

# Send a message
curl -X POST http://localhost:5001/api/messages \
  -H "Content-Type: application/json" \
  -d '{"content":"Hello!", "sender":"user", "conversationId":"conv_001"}'
```

## 🛑 Stopping the Application

Press `Ctrl+C` in the terminal where the servers are running, or use the startup script which handles cleanup automatically.

## 🔮 Future Enhancements

- Real AI integration (OpenAI, Gemini API)
- User authentication
- Real database (MongoDB, PostgreSQL)
- WebSocket for real-time messaging
- File upload support
- Message search functionality
