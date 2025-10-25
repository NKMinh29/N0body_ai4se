import mongoose, { Document, Schema } from 'mongoose';

export interface IMessage extends Document {
  content: string;
  sender: 'user' | 'assistant';
  timestamp: Date;
  conversationId?: string;
}

const MessageSchema = new Schema<IMessage>({
  content: {
    type: String,
    required: true,
  },
  sender: {
    type: String,
    enum: ['user', 'assistant'],
    required: true,
  },
  timestamp: {
    type: Date,
    default: Date.now,
  },
  conversationId: {
    type: String,
    default: () => new mongoose.Types.ObjectId().toString(),
  },
});

export default mongoose.models.Message || mongoose.model<IMessage>('Message', MessageSchema);
