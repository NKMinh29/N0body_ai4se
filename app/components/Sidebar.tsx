'use client';

import { useState, useEffect } from 'react';
import { externalAPI } from '../services/externalAPI';

interface SidebarProps {
  isOpen: boolean;
  onToggle: () => void;
  onConversationSelect?: (conversationId: string) => void;
  onNewChat?: () => void;
}

interface Conversation {
  id: string;
  title: string;
  lastMessage: string;
  timestamp: string;
  messageCount: number;
}

export default function Sidebar({ isOpen, onToggle, onConversationSelect, onNewChat }: SidebarProps) {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchConversations();
  }, []);

  const formatLastUpdated = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`;
    
    return date.toLocaleDateString('en-US', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const fetchConversations = async () => {
    try {
      const data = await externalAPI.getConversations();
      setConversations(data.conversations || []);
    } catch (error) {
      console.error('Error fetching conversations:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleNewChat = () => {
    onNewChat?.();
    // Refresh conversations after creating new chat
    fetchConversations();
  };

  return (
    <div className={`${isOpen ? 'w-80' : 'w-0'} transition-all duration-300 overflow-hidden bg-gray-800 border-r border-gray-700`}>
      <div className="flex flex-col h-full">
        {/* Top Navigation */}
        <div className="p-4 space-y-2">
          <button 
            onClick={handleNewChat}
            className="w-full flex items-center gap-3 px-3 py-2 text-white hover:bg-gray-700 rounded-lg transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            <span className="text-sm font-medium">Cuộc trò chuyện mới</span>
            <svg className="w-4 h-4 ml-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
          </button>
        </div>

        {/* Recent Chats */}
        <div className="flex-1 px-4 pb-4">
          <h3 className="text-xs font-medium text-gray-400 uppercase tracking-wider mb-3">Gần đây</h3>
          <div className="space-y-1">
            {loading ? (
              <div className="text-center text-gray-400 text-sm py-4">Đang tải...</div>
            ) : conversations.length === 0 ? (
              <div className="text-center text-gray-400 text-sm py-4">Chưa có cuộc trò chuyện nào</div>
            ) : (
              conversations.map((conversation) => (
                <button
                  key={conversation.id}
                  onClick={() => onConversationSelect?.(conversation.id)}
                  className="w-full text-left px-3 py-2 text-sm text-white hover:bg-gray-700 rounded-lg transition-colors"
                  title={conversation.title}
                >
                  <div className="truncate mb-1">
                    {conversation.title.length > 50 
                      ? `${conversation.title.substring(0, 50)}...` 
                      : conversation.title}
                  </div>
                  <div className="text-xs text-gray-400">
                    {formatLastUpdated(conversation.timestamp)}
                  </div>
                </button>
              ))
            )}
          </div>
        </div>

        {/* Bottom Navigation */}
        <div className="p-4 border-t border-gray-700">
          <button className="w-full flex items-center gap-3 px-3 py-2 text-white hover:bg-gray-700 rounded-lg transition-colors">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <span className="text-sm font-medium">Cài đặt và trợ giúp</span>
          </button>
        </div>
      </div>
    </div>
  );
}