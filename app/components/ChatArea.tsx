'use client';

import { useState, useEffect, useRef } from 'react';
import { externalAPI } from '../services/externalAPI';

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: string;
}

interface ChatAreaProps {
  selectedConversationId?: string;
  aiMode?: 'math' | 'english' | 'history' | 'general';
}

export default function ChatArea({ selectedConversationId, aiMode = 'general' }: ChatAreaProps) {
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentConversationId, setCurrentConversationId] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [conversationTitle, setConversationTitle] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (selectedConversationId) {
      loadConversation(selectedConversationId);
    } else {
      // Generate a new conversation ID when no conversation is selected
      setCurrentConversationId(new Date().getTime().toString());
      setMessages([]);
      setConversationTitle('');
    }
  }, [selectedConversationId]);

  const generateAIResponse = (userMessage: string, mode: string): string => {
    const responses = {
      math: [
        `Let me help you solve this mathematical problem step by step. First, let's identify what we're working with: "${userMessage}".`,
        `I'll guide you through this math concept. The key to understanding "${userMessage}" is to break it down systematically.`,
        `As your math tutor, I'll explain "${userMessage}" using clear examples and step-by-step solutions.`,
        `Let's work through this mathematical challenge together. For "${userMessage}", we need to consider the fundamental principles.`
      ],
      english: [
        `Let me help you improve your English! For "${userMessage}", I'll explain the grammar, vocabulary, and usage.`,
        `As your English teacher, I'll guide you through proper language usage. "${userMessage}" is a great example to learn from.`,
        `I'll help you understand the nuances of English language. Let's analyze "${userMessage}" together.`,
        `Let's practice English together! For "${userMessage}", I'll show you correct pronunciation, grammar, and context.`
      ],
      history: [
        `Let me share the historical context of "${userMessage}". This is a fascinating period in history with many important events.`,
        `As your history teacher, I'll explain the significance of "${userMessage}" in the broader historical timeline.`,
        `Let's explore the historical background of "${userMessage}". This topic connects to many important historical events.`,
        `I'll help you understand the historical importance of "${userMessage}" and its impact on society.`
      ],
      general: [
        `I understand you're asking about: "${userMessage}". This is an interesting topic!`,
        `Let me help you with: "${userMessage}". I'll provide you with comprehensive information.`,
        `That's a great question about "${userMessage}". Let me explain this in detail.`,
        `I'd be happy to help you understand "${userMessage}". Here's what I can tell you.`
      ]
    };

    const modeResponses = responses[mode as keyof typeof responses] || responses.general;
    return modeResponses[Math.floor(Math.random() * modeResponses.length)];
  };

  const loadConversation = async (conversationId: string) => {
    try {
      setLoading(true);
      const data = await externalAPI.getConversation(conversationId);
      
      if (data.status === 'success') {
        setCurrentConversationId(conversationId);
        setMessages(data.messages || []);
        setConversationTitle(data.conversation?.title || '');
      }
    } catch (error) {
      console.error('Error loading conversation:', error);
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: 'user',
      timestamp: new Date().toISOString(),
    };

    // Add user message immediately
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setLoading(true);

    try {
      console.log('Sending message:', userMessage.content, 'Mode:', aiMode);
      
      // Save user message to external backend
      await externalAPI.createMessage(userMessage.content, userMessage.sender, currentConversationId);
      console.log('User message saved to external backend');

      // Get AI response from external backend
      const aiData = await externalAPI.getAIResponse(userMessage.content, aiMode, currentConversationId);
      console.log('AI response received:', aiData);
      
      if (aiData.status === 'success') {
        const aiMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: aiData.response,
          sender: 'assistant',
          timestamp: new Date().toISOString(),
        };

        setMessages(prev => [...prev, aiMessage]);
        setLoading(false);
        console.log('AI message added to chat');

        // Save AI response to external backend
        await externalAPI.createMessage(aiMessage.content, aiMessage.sender, currentConversationId);
        console.log('AI message saved to external backend');
      } else {
        console.log('AI response failed, using fallback');
        // Fallback response if AI fails
        const fallbackMessage: Message = {
          id: (Date.now() + 1).toString(),
          content: generateAIResponse(userMessage.content, aiMode),
          sender: 'assistant',
          timestamp: new Date().toISOString(),
        };

        setMessages(prev => [...prev, fallbackMessage]);
        setLoading(false);

        // Save fallback response to external backend
        await externalAPI.createMessage(fallbackMessage.content, fallbackMessage.sender, currentConversationId);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Fallback response on error
      const fallbackMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: generateAIResponse(userMessage.content, aiMode),
        sender: 'assistant',
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, fallbackMessage]);
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex-1 flex flex-col bg-gray-900">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-800">
        {loading && messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400"></div>
            <p className="text-gray-400 text-lg mt-4">Đang tải cuộc trò chuyện...</p>
          </div>
        ) : messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full">
            <h2 className="text-4xl font-bold text-blue-400 mb-2">
              {conversationTitle ? conversationTitle : "Chào bạn! Minh - N0b0dy"}
            </h2>
            <p className="text-gray-400 text-lg">Hãy bắt đầu cuộc trò chuyện của bạn</p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  message.sender === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-700 text-white'
                }`}
              >
                <p className="text-sm">{message.content}</p>
                <p className="text-xs opacity-70 mt-1">
                  {new Date(message.timestamp).toLocaleTimeString()}
                </p>
              </div>
            </div>
          ))
        )}
        
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-700 text-white px-4 py-2 rounded-lg">
              <div className="flex items-center space-x-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span className="text-sm">Đang suy nghĩ...</span>
              </div>
            </div>
          </div>
        )}
        
        {/* Scroll anchor */}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 border-t border-gray-700">
        <div className="relative bg-gray-800 rounded-2xl border border-gray-600 p-4">
          <div className="flex items-center gap-3">
            {/* Left Controls */}
            <button className="p-2 hover:bg-gray-700 rounded-full transition-colors">
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
            </button>
            
            <button className="p-2 hover:bg-gray-700 rounded-full transition-colors">
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
              </svg>
            </button>
            <span className="text-xs text-gray-400">Công cụ</span>

            {/* Input Field */}
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask N0b0dy"
              className="flex-1 bg-transparent text-white placeholder-gray-400 outline-none text-lg"
              disabled={loading}
            />

            {/* Right Controls */}
            <div className="flex items-center gap-2">
              <div className="flex items-center gap-1 px-2 py-1 bg-gray-700 rounded-lg">
                <span className="text-sm text-white">2.5 Pro</span>
                <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </div>
              
              <button 
                onClick={sendMessage}
                disabled={!inputValue.trim() || loading}
                className="p-2 hover:bg-gray-700 rounded-full transition-colors disabled:opacity-50"
              >
                <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}