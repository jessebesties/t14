
import React from 'react';
import MarketSidebar from '@/components/MarketSidebar';
import ChatInterface from '@/components/ChatInterface';

const Index = () => {
  return (
    <div className="min-h-screen bg-background flex w-full">
      {/* Left Sidebar - Market Intelligence */}
      <MarketSidebar />
      
      {/* Main Chat Interface */}
      <ChatInterface />
    </div>
  );
};

export default Index;
