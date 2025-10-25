import { NextRequest, NextResponse } from 'next/server';
import mongoose from 'mongoose';
import connectDB from '@/lib/mongodb';
import Message from '@/models/Message';

// GET /api/messages - Fetch all messages
export async function GET(request: NextRequest) {
  try {
    await connectDB();
    
    const { searchParams } = new URL(request.url);
    const conversationId = searchParams.get('conversationId');
    
    let query = {};
    if (conversationId) {
      query = { conversationId };
    }
    
    const messages = await Message.find(query).sort({ timestamp: 1 });
    
    return NextResponse.json({ messages });
  } catch (error) {
    console.error('Error fetching messages:', error);
    return NextResponse.json(
      { error: 'Failed to fetch messages' },
      { status: 500 }
    );
  }
}

// POST /api/messages - Create a new message
export async function POST(request: NextRequest) {
  try {
    await connectDB();
    
    const { content, sender, conversationId } = await request.json();
    
    if (!content || !sender) {
      return NextResponse.json(
        { error: 'Content and sender are required' },
        { status: 400 }
      );
    }
    
    const message = new Message({
      content,
      sender,
      conversationId: conversationId || new mongoose.Types.ObjectId().toString(),
    });
    
    await message.save();
    
    return NextResponse.json({ message }, { status: 201 });
  } catch (error) {
    console.error('Error creating message:', error);
    return NextResponse.json(
      { error: 'Failed to create message' },
      { status: 500 }
    );
  }
}
