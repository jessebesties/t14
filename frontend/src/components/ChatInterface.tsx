import React, { useState, useRef, useEffect } from 'react';
import { Send, Plus, TrendingUp, Newspaper, Search, Zap, Bot, User, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

const ChatInterface = () => {
  const [message, setMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: "Hi! I'm FinBot, your AI market intelligence assistant. I can help you analyze stocks, track market movements, and break down complex financial news. What would you like to explore today?",
      timestamp: new Date(),
    },
  ]);

  const suggestionChips = [
    {
      icon: TrendingUp,
      text: 'Market Movers',
      description: 'Show me the biggest gainers and losers today',
      color: 'bg-gradient-to-r from-green-500/20 to-emerald-500/20 text-green-400 border-green-500/30 hover:from-green-500/30 hover:to-emerald-500/30',
    },
    {
      icon: Newspaper,
      text: 'Breaking News',
      description: 'What news is moving markets right now?',
      color: 'bg-gradient-to-r from-orange-500/20 to-red-500/20 text-orange-400 border-orange-500/30 hover:from-orange-500/30 hover:to-red-500/30',
    },
    {
      icon: Search,
      text: 'Stock Analysis',
      description: 'Analyze AAPL for me',
      color: 'bg-gradient-to-r from-blue-500/20 to-cyan-500/20 text-blue-400 border-blue-500/30 hover:from-blue-500/30 hover:to-cyan-500/30',
    },
    {
      icon: Zap,
      text: 'Tech Sector',
      description: "What's happening with TSLA?",
      color: 'bg-gradient-to-r from-purple-500/20 to-pink-500/20 text-purple-400 border-purple-500/30 hover:from-purple-500/30 hover:to-pink-500/30',
    },
  ];

  const quickActions = [
    { text: "What's moving the market?", icon: TrendingUp },
    { text: "Analyze NVDA", icon: Zap },
    { text: "Analyze AAPL", icon: Search },
    { text: "What about TSLA?", icon: Sparkles },
  ];

  // Check backend connection on component mount
  useEffect(() => {
    checkBackendConnection();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const checkBackendConnection = async () => {
    try {
      const response = await fetch('http://localhost:8000/health');
      if (response.ok) {
        setIsConnected(true);
      } else {
        setIsConnected(false);
      }
    } catch (error) {
      console.error('Backend connection failed:', error);
      setIsConnected(false);
    }
  };

  const sendMessageToBackend = async (userMessage: string) => {
    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.success) {
        return data.response;
      } else {
        return "Sorry, I encountered an error while processing your request. Please try again.";
      }
    } catch (error) {
      console.error('Error sending message to backend:', error);
      return "I'm having trouble connecting to the market data service. Please check if the backend is running and try again.";
    }
  };

  const handleSendMessage = async () => {
    if (!message.trim()) return;

    const newMessage = {
      id: Date.now(),
      type: 'user',
      content: message,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, newMessage]);
    setMessage('');
    setIsTyping(true);

    // Send to backend and get real response
    const botResponseContent = await sendMessageToBackend(newMessage.content);

    setTimeout(() => {
      const botResponse = {
        id: Date.now() + 1,
        type: 'bot',
        content: botResponseContent,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, botResponse]);
      setIsTyping(false);
    }, 500);
  };

  const handleChipClick = (chip: any) => {
    setMessage(chip.description);
    setTimeout(() => handleSendMessage(), 100);
  };

  const handleQuickAction = (action: any) => {
    setMessage(action.text);
    setTimeout(() => handleSendMessage(), 100);
  };

  return (
    <div className="flex-1 flex flex-col h-screen chart-bg">
      {/* Header */}
      <div className="border-b border-border/30 bg-card/30 backdrop-blur-xl p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-primary to-primary/60 rounded-xl flex items-center justify-center">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold gradient-text">FinBot Assistant</h1>
              <p className="text-xs text-muted-foreground">AI Market Intelligence • Real-time Analysis</p>
            </div>
          </div>
          <Badge variant="outline" className="text-xs">
            <div className={`w-2 h-2 rounded-full mr-2 ${isConnected ? 'bg-green-400 market-pulse' : 'bg-red-400'}`}></div>
            {isConnected ? 'Live Market Data' : 'Disconnected'}
          </Badge>
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex gap-4 ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {msg.type === 'bot' && (
              <div className="w-8 h-8 bg-gradient-to-br from-primary to-primary/60 rounded-lg flex items-center justify-center flex-shrink-0">
                <Bot className="w-4 h-4 text-white" />
              </div>
            )}
            
            <div
              className={`max-w-2xl ${
                msg.type === 'user'
                  ? 'bg-gradient-to-br from-primary to-primary/80 text-white rounded-2xl rounded-tr-sm'
                  : 'glass-card rounded-2xl rounded-tl-sm'
              } p-4 shadow-lg`}
            >
              {msg.type === 'bot' && (
                <div className="flex items-center gap-2 mb-3">
                  <span className="text-sm font-semibold text-primary">FinBot</span>
                  <Badge variant="secondary" className="text-xs">
                    AI Assistant
                  </Badge>
                </div>
              )}
              <div className="text-sm leading-relaxed whitespace-pre-line">{msg.content}</div>
              <p className="text-xs opacity-60 mt-3">
                {msg.timestamp.toLocaleTimeString()}
              </p>
            </div>

            {msg.type === 'user' && (
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-500 rounded-lg flex items-center justify-center flex-shrink-0">
                <User className="w-4 h-4 text-white" />
              </div>
            )}
          </div>
        ))}

        {isTyping && (
          <div className="flex gap-4 justify-start">
            <div className="w-8 h-8 bg-gradient-to-br from-primary to-primary/60 rounded-lg flex items-center justify-center flex-shrink-0">
              <Bot className="w-4 h-4 text-white" />
            </div>
            <div className="glass-card rounded-2xl rounded-tl-sm p-4">
              <div className="flex items-center gap-2">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-primary rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                  <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                </div>
                <span className="text-xs text-muted-foreground">FinBot is analyzing market data...</span>
              </div>
            </div>
          </div>
        )}

        {/* Suggestion Chips - Only show initially */}
        {messages.length === 1 && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8">
            {suggestionChips.map((chip, index) => (
              <Card
                key={index}
                className={`cursor-pointer transition-all duration-300 hover:scale-105 transform ${chip.color} border trading-card`}
                onClick={() => handleChipClick(chip)}
              >
                <CardContent className="p-4">
                  <div className="flex items-start gap-3">
                    <div className="p-2 rounded-lg bg-current/10">
                      <chip.icon className="w-5 h-5" />
                    </div>
                    <div className="flex-1">
                      <h3 className="font-semibold text-sm mb-1">{chip.text}</h3>
                      <p className="text-xs opacity-80 leading-relaxed">{chip.description}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Message Input */}
      <div className="border-t border-border/30 bg-card/30 backdrop-blur-xl p-4">
        <div className="max-w-4xl mx-auto space-y-3">
          {/* Connection Status */}
          {!isConnected && (
            <div className="text-center p-3 bg-red-500/10 border border-red-500/30 rounded-lg">
              <p className="text-sm text-red-400">
                ⚠️ Not connected to market data service. Make sure the backend is running on http://localhost:8000
              </p>
              <Button 
                variant="outline" 
                size="sm" 
                className="mt-2 text-xs" 
                onClick={checkBackendConnection}
              >
                Retry Connection
              </Button>
            </div>
          )}
          
          <div className="flex gap-3">
            <div className="flex-1 relative">
              <Input
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Ask about any stock, market move, or news event..."
                className="pr-12 bg-card/50 backdrop-blur-sm border-border/50 h-12 text-sm"
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                disabled={!isConnected}
              />
              <Button
                onClick={handleSendMessage}
                className="absolute right-1 top-1 h-10 w-10 p-0 action-button"
                disabled={!message.trim() || isTyping || !isConnected}
              >
                <Send className="w-4 h-4" />
              </Button>
            </div>
          </div>
          
          {/* Quick Actions */}
          <div className="flex flex-wrap gap-2">
            {quickActions.map((action, index) => (
              <Button
                key={index}
                variant="outline"
                size="sm"
                className="text-xs h-7 bg-card/30 backdrop-blur-sm border-border/30 hover:bg-card/50"
                onClick={() => handleQuickAction(action)}
                disabled={!isConnected}
              >
                <action.icon className="w-3 h-3 mr-1" />
                {action.text}
              </Button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
