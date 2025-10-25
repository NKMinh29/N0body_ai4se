'use client';

import { useState, useEffect } from 'react';
import { externalAPI } from '../services/externalAPI';

interface SearchResult {
  conversationId: string;
  conversationTitle: string;
  messageId: string;
  content: string;
  sender: 'user' | 'assistant';
  timestamp: string;
}

interface SearchResultsProps {
  query: string;
  onClose: () => void;
  onResultClick: (conversationId: string) => void;
}

export default function SearchResults({ query, onClose, onResultClick }: SearchResultsProps) {
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (query.trim()) {
      searchMessages(query);
    }
  }, [query]);

  const searchMessages = async (searchQuery: string) => {
    setLoading(true);
    try {
      const data = await externalAPI.searchMessages(searchQuery);
      setResults(data.results || []);
    } catch (error) {
      console.error('Error searching messages:', error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const formatTimestamp = (timestamp: string) => {
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

  const highlightText = (text: string, query: string) => {
    const regex = new RegExp(`(${query})`, 'gi');
    const parts = text.split(regex);
    
    return parts.map((part, index) => 
      regex.test(part) ? (
        <mark key={index} className="bg-yellow-300 text-black px-1 rounded">
          {part}
        </mark>
      ) : part
    );
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-800 rounded-lg w-full max-w-4xl max-h-[80vh] overflow-hidden">
        <div className="flex items-center justify-between p-4 border-b border-gray-700">
          <h2 className="text-xl font-bold text-white">
            Search Results for "{query}"
          </h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
          >
            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div className="overflow-y-auto max-h-[60vh] p-4">
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400"></div>
              <span className="ml-3 text-gray-400">Searching...</span>
            </div>
          ) : results.length === 0 ? (
            <div className="text-center text-gray-400 py-8">
              No results found for "{query}"
            </div>
          ) : (
            <div className="space-y-4">
              {results.map((result) => (
                <div
                  key={`${result.conversationId}-${result.messageId}`}
                  className="bg-gray-700 rounded-lg p-4 hover:bg-gray-600 transition-colors cursor-pointer"
                  onClick={() => {
                    onResultClick(result.conversationId);
                    onClose();
                  }}
                >
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-medium text-white truncate">
                      {result.conversationTitle}
                    </h3>
                    <span className="text-xs text-gray-400 ml-2 shrink-0">
                      {formatTimestamp(result.timestamp)}
                    </span>
                  </div>
                  
                  <div className="flex items-center gap-2 mb-2">
                    <span className={`text-xs px-2 py-1 rounded ${
                      result.sender === 'user' 
                        ? 'bg-blue-600 text-white' 
                        : 'bg-gray-600 text-white'
                    }`}>
                      {result.sender === 'user' ? 'You' : 'N0b0dy'}
                    </span>
                  </div>
                  
                  <p className="text-gray-300 text-sm leading-relaxed">
                    {highlightText(result.content, query)}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
        
        <div className="p-4 border-t border-gray-700 text-center text-gray-400 text-sm">
          Found {results.length} result{results.length !== 1 ? 's' : ''}
        </div>
      </div>
    </div>
  );
}
