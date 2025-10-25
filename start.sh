#!/bin/bash

echo "🚀 Starting Gemini Chat Application with Python Backend"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd backend
pip3 install -r requirements.txt

# Start Python backend
echo "🐍 Starting Python Flask Backend on port 5000..."
python3 app.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Go back to project root
cd ..

# Start Next.js frontend
echo "⚛️  Starting Next.js Frontend on port 3000..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Both servers are starting up!"
echo "🌐 Frontend: http://localhost:3000"
echo "🐍 Backend: http://localhost:5000"
echo ""
echo "📡 Backend API Endpoints:"
echo "   - GET  http://localhost:5000/api/conversations"
echo "   - GET  http://localhost:5000/api/messages?conversationId=<id>"
echo "   - POST http://localhost:5000/api/messages"
echo "   - GET  http://localhost:5000/api/conversation/<id>"
echo "   - GET  http://localhost:5000/api/health"
echo ""
echo "🛑 Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for both processes
wait
