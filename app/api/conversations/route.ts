import { NextRequest, NextResponse } from 'next/server';
import connectDB from '@/lib/mongodb';
import Message from '@/models/Message';

// GET /api/conversations - Fetch recent conversations
export async function GET(request: NextRequest) {
  try {
    await connectDB();
    
    // Get unique conversation IDs with their latest message
    const conversations = await Message.aggregate([
      {
        $sort: { timestamp: -1 }
      },
      {
        $group: {
          _id: '$conversationId',
          latestMessage: { $first: '$content' },
          timestamp: { $first: '$timestamp' },
          messageCount: { $sum: 1 }
        }
      },
      {
        $sort: { timestamp: -1 }
      },
      {
        $limit: 20
      }
    ]);
    
    return NextResponse.json({ conversations });
  } catch (error) {
    console.error('Error fetching conversations:', error);
    return NextResponse.json(
      { error: 'Failed to fetch conversations' },
      { status: 500 }
    );
  }
}
