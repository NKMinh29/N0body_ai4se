'use client';

import { useState } from 'react';
import Sidebar from './Sidebar';
import Header from './Header';
import ChatArea from './ChatArea';
import FloatingButton from './FloatingButton';
import SearchResults from './SearchResults';

export default function ChatInterface() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [selectedConversationId, setSelectedConversationId] = useState<string | undefined>();
  const [aiMode, setAiMode] = useState<'math' | 'english' | 'history' | 'general'>('general');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [showSearchResults, setShowSearchResults] = useState(false);

  const handleConversationSelect = (conversationId: string) => {
    setSelectedConversationId(conversationId);
  };

  const handleNewChat = () => {
    setSelectedConversationId(undefined);
  };

  const handleModeChange = (mode: 'math' | 'english' | 'history' | 'general') => {
    setAiMode(mode);
  };

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    setShowSearchResults(true);
  };

  const handleSearchResultClick = (conversationId: string) => {
    setSelectedConversationId(conversationId);
  };

  const handleCloseSearchResults = () => {
    setShowSearchResults(false);
    setSearchQuery('');
  };

  return (
    <div className="flex h-screen bg-gray-900 text-white">
      {/* Sidebar */}
      <Sidebar 
        isOpen={sidebarOpen} 
        onToggle={() => setSidebarOpen(!sidebarOpen)}
        onConversationSelect={handleConversationSelect}
        onNewChat={handleNewChat}
      />
      
      {/* Main Content Area */}
      <div className="flex flex-col flex-1">
        {/* Header */}
        <Header 
          onMenuClick={() => setSidebarOpen(!sidebarOpen)}
          onModeChange={handleModeChange}
          currentMode={aiMode}
          onSearch={handleSearch}
        />
        
        {/* Chat Area */}
        <ChatArea 
          selectedConversationId={selectedConversationId}
          aiMode={aiMode}
        />
      </div>
      
      {/* Floating Button */}
      <FloatingButton />
      
      {/* Search Results Modal */}
      {showSearchResults && (
        <SearchResults
          query={searchQuery}
          onClose={handleCloseSearchResults}
          onResultClick={handleSearchResultClick}
        />
      )}
    </div>
  );
}

