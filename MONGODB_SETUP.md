# MongoDB Setup Instructions

## Prerequisites
1. Install MongoDB locally or use MongoDB Atlas
2. Create a `.env.local` file in the root directory with:
   ```
   MONGODB_URI=mongodb://localhost:27017/gemini-chat
   ```

## For Local MongoDB:
1. Install MongoDB Community Edition
2. Start MongoDB service: `mongod`
3. The app will automatically create the database and collections

## For MongoDB Atlas:
1. Create a free cluster at https://cloud.mongodb.com
2. Get your connection string
3. Update `.env.local` with your Atlas connection string

## Running the Application:
1. Start MongoDB (if using local)
2. Run: `npm run dev`
3. Open http://localhost:3000

## Features Implemented:
- ✅ MongoDB integration with Mongoose
- ✅ Message storage and retrieval
- ✅ Conversation history
- ✅ Real-time chat interface
- ✅ API endpoints for messages and conversations
- ✅ Clean frontend without hardcoded data
