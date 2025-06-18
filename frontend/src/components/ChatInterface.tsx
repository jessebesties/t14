
import React, { useState, useRef, useEffect } from 'react';
import { Send, Plus, TrendingUp, Newspaper, Search, Zap, Bot, User, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

const ChatInterface = () => {
  const [message, setMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
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
      description: 'Analyze a specific ticker for me',
      color: 'bg-gradient-to-r from-blue-500/20 to-cyan-500/20 text-blue-400 border-blue-500/30 hover:from-blue-500/30 hover:to-cyan-500/30',
    },
    {
      icon: Zap,
      text: 'Tech Sector',
      description: "What's happening in tech stocks?",
      color: 'bg-gradient-to-r from-purple-500/20 to-pink-500/20 text-purple-400 border-purple-500/30 hover:from-purple-500/30 hover:to-pink-500/30',
    },
  ];

  const quickActions = [
    { text: "What's moving the market?", icon: TrendingUp },
    { text: "Unusual options activity", icon: Zap },
    { text: "Analyze AAPL", icon: Search },
    { text: "Sector rotation update", icon: Sparkles },
  ];

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

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

    // Simulate bot response with typing delay
    setTimeout(() => {
      const botResponse = {
        id: Date.now() + 1,
        type: 'bot',
        content: getBotResponse(newMessage.content),
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, botResponse]);
      setIsTyping(false);
    }, 1500);
  };

  const getBotResponse = (userMessage: string) => {
    const lower = userMessage.toLowerCase();
    
    if (lower.includes('nvda') || lower.includes('nvidia')) {
      return "🚀 **NVDA Analysis**: Strong momentum today with +4.2% gains to $485.23\n\n📈 **Key Levels**: Resistance at $490, Support at $470\n📊 **Volume**: 2.3x average (very bullish)\n💡 **Catalyst**: Better-than-expected earnings + raised guidance\n\n**Related plays**: AMD (+2.9%), AVGO, TSM showing sympathy moves. Semiconductor sector rotating strong with unusual call activity.\n\nWant me to dive deeper into the options flow or check other semi plays?";
    }
    
    if (lower.includes('market movers') || lower.includes('gainers') || lower.includes('moving')) {
      return "📊 **Today's Market Leaders**:\n\n🟢 **Top Gainers**:\n• NVDA: +4.2% - Earnings beat driving semi rally\n• TSLA: +3.8% - Delivery optimism building\n• AMD: +2.9% - Riding NVDA coattails\n\n🔴 **Notable Declines**:\n• META: -3.1% - New regulatory headwinds\n• NFLX: -2.4% - Sector rotation out of streaming\n\n**🎯 Key Observation**: Semiconductor rotation is the strongest we've seen this week. Tech leading overall market.\n\nWhich sector interests you most?";
    }
    
    if (lower.includes('news') || lower.includes('breaking')) {
      return "⚡ **Market-Moving Headlines**:\n\n🔥 **Top Priority**:\n1. **NVDA Earnings Beat** - Driving 4%+ rally, lifting entire semi sector\n2. **Fed Rate Pause Signals** - Officials hinting at potential pause next meeting\n\n📰 **Also Watching**:\n3. **META Regulatory Pressure** - New antitrust concerns weighing on stock\n4. **Oil Supply Concerns** - Crude up 2.1% on geopolitical tensions\n\nThe NVDA story is creating the biggest sector rotation this week. Tech money flowing fast.\n\n**Need specifics on any of these stories?**";
    }
    
    if (lower.includes('aapl') || lower.includes('apple')) {
      return "🍎 **AAPL Technical Snapshot**:\n\n📈 **Current**: $178.45 (+0.8%)\n🎯 **Key Levels**: Support $175 | Resistance $182\n📊 **Volume**: Below average (consolidation mode)\n\n**📱 Upcoming Catalysts**:\n• iPhone 15 production ramp\n• Services growth trajectory\n• China market recovery signs\n\n**Options Activity**: Calls slightly favored, but nothing unusual. AAPL in wait-and-see mode while market focuses on AI/semiconductor plays.\n\nWant technical analysis or fundamental deep-dive?";
    }
    
    return "I'm analyzing that for you right now... 🔍\n\nCould you be more specific about which aspect interests you most? I can provide:\n\n📊 **Technical Analysis** - Price levels, volume, momentum\n📰 **News Impact** - How headlines are moving prices\n💹 **Options Flow** - What smart money is doing\n🏢 **Sector Analysis** - Rotation patterns and themes\n\nWhat would be most helpful for your trading decisions?";
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
            <div className="w-2 h-2 bg-green-400 rounded-full mr-2 market-pulse"></div>
            Live Market Data
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
                <span className="text-xs text-muted-foreground">FinBot is analyzing...</span>
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
          <div className="flex gap-3">
            <div className="flex-1 relative">
              <Input
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Ask about any stock, market move, or news event..."
                className="pr-12 bg-card/50 backdrop-blur-sm border-border/50 h-12 text-sm"
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              />
              <Button
                onClick={handleSendMessage}
                className="absolute right-1 top-1 h-10 w-10 p-0 action-button"
                disabled={!message.trim() || isTyping}
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
