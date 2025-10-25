'use client';

import { useState } from 'react';

interface HeaderProps {
  onMenuClick: () => void;
  onModeChange?: (mode: 'math' | 'english' | 'history' | 'general') => void;
  currentMode?: 'math' | 'english' | 'history' | 'general';
  onSearch?: (query: string) => void;
}

export default function Header({ onMenuClick, onModeChange, currentMode = 'general', onSearch }: HeaderProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [showSearchInput, setShowSearchInput] = useState(false);

  const handleSearch = () => {
    if (searchQuery.trim()) {
      onSearch?.(searchQuery.trim());
      setSearchQuery('');
      setShowSearchInput(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };
  return (
    <header className="flex items-center justify-between px-4 py-3 bg-gray-900 border-b border-gray-700">
      {/* Left Side */}
      <div className="flex items-center gap-4">
        <button
          onClick={onMenuClick}
          className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        
        <button 
          onClick={() => setShowSearchInput(!showSearchInput)}
          className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </button>
        
        {showSearchInput && (
          <div className="flex items-center gap-2">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Search messages..."
              className="px-3 py-1 bg-gray-800 text-white rounded-lg border border-gray-600 focus:outline-none focus:border-blue-500"
              autoFocus
            />
            <button
              onClick={handleSearch}
              className="px-3 py-1 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Search
            </button>
          </div>
        )}
        
        <h1 className="text-xl font-bold text-white">N0b0dy</h1>
      </div>

      {/* Mode Selection Buttons */}
      <div className="flex items-center gap-2">
        <button
          onClick={() => onModeChange?.('math')}
          className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
            currentMode === 'math' 
              ? 'bg-blue-600 text-white' 
              : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
          }`}
        >
          Math
        </button>
        <button
          onClick={() => onModeChange?.('english')}
          className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
            currentMode === 'english' 
              ? 'bg-blue-600 text-white' 
              : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
          }`}
        >
          English
        </button>
        <button
          onClick={() => onModeChange?.('history')}
          className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
            currentMode === 'history' 
              ? 'bg-blue-600 text-white' 
              : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
          }`}
        >
          History
        </button>
      </div>

      {/* Right Side */}
      <div className="flex items-center gap-3">
        <span className="text-sm font-medium text-white bg-blue-600 px-2 py-1 rounded">PRO</span>
        
        {/* Profile Picture */}
        <div className="w-8 h-8 rounded-full bg-linear-to-br from-red-500 via-yellow-500 to-green-500 p-0.5">
          <div className="w-full h-full rounded-full bg-gray-800 flex items-center justify-center">
            <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
            </svg>
          </div>
        </div>
      </div>
    </header>
  );
}
