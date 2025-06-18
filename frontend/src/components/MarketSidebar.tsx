
import React, { useState } from 'react';
import { TrendingUp, TrendingDown, AlertTriangle, Clock, BarChart3, Zap, Eye, Bell } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';

const MarketSidebar = () => {
  const [activeTab, setActiveTab] = useState('pulse');

  // Mock data - in a real app this would come from APIs
  const marketIndices = [
    { name: 'S&P 500', value: '4,567.23', change: '+0.8%', trend: 'up', points: '+18.45' },
    { name: 'NASDAQ', value: '14,234.56', change: '+1.2%', trend: 'up', points: '+168.90' },
    { name: 'DOW', value: '35,678.90', change: '-0.3%', trend: 'down', points: '-107.23' },
  ];

  const topMovers = {
    gainers: [
      { symbol: 'NVDA', change: '+4.2%', price: '$485.23', volume: '2.3M' },
      { symbol: 'TSLA', change: '+3.8%', price: '$242.67', volume: '1.8M' },
      { symbol: 'AMD', change: '+2.9%', price: '$145.89', volume: '950K' },
      { symbol: 'MSFT', change: '+2.1%', price: '$378.45', volume: '1.2M' },
      { symbol: 'GOOGL', change: '+1.7%', price: '$142.33', volume: '890K' },
    ],
    losers: [
      { symbol: 'META', change: '-3.1%', price: '$334.22', volume: '2.1M' },
      { symbol: 'NFLX', change: '-2.4%', price: '$445.67', volume: '750K' },
      { symbol: 'PYPL', change: '-1.9%', price: '$67.89', volume: '1.5M' },
      { symbol: 'UBER', change: '-1.6%', price: '$56.34', volume: '680K' },
      { symbol: 'SNAP', change: '-1.3%', price: '$12.45', volume: '3.2M' },
    ],
  };

  const breakingNews = [
    { 
      headline: 'NVDA beats earnings, raises guidance', 
      time: '2m ago', 
      impact: 'high',
      isBreaking: true
    },
    { 
      headline: 'Fed signals potential rate pause', 
      time: '15m ago', 
      impact: 'high',
      isBreaking: false
    },
    { 
      headline: 'META faces new regulatory scrutiny', 
      time: '32m ago', 
      impact: 'medium',
      isBreaking: false
    },
    { 
      headline: 'Oil prices surge on supply concerns', 
      time: '1h ago', 
      impact: 'medium',
      isBreaking: false
    },
    { 
      headline: 'Tech sector shows unusual options flow', 
      time: '1h ago', 
      impact: 'low',
      isBreaking: false
    },
  ];

  const tabs = [
    { id: 'pulse', label: 'Pulse', icon: BarChart3 },
    { id: 'news', label: 'News', icon: Bell },
    { id: 'movers', label: 'Movers', icon: TrendingUp },
  ];

  return (
    <div className="w-80 glass-card p-4 space-y-4 overflow-y-auto h-screen border-r">
      {/* Header with tabs */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold gradient-text">Market Intelligence</h2>
          <div className="flex items-center gap-1">
            <div className="w-2 h-2 bg-green-400 rounded-full market-pulse"></div>
            <span className="text-xs text-green-400">Live</span>
          </div>
        </div>

        <div className="flex bg-muted/30 p-1 rounded-lg">
          {tabs.map((tab) => (
            <Button
              key={tab.id}
              variant={activeTab === tab.id ? "default" : "ghost"}
              size="sm"
              className={`flex-1 h-8 text-xs ${activeTab === tab.id ? 'action-button' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              <tab.icon className="w-3 h-3 mr-1" />
              {tab.label}
            </Button>
          ))}
        </div>
      </div>

      {/* Tab Content */}
      {activeTab === 'pulse' && (
        <>
          {/* Live Market Pulse */}
          <Card className="trading-card">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm flex items-center gap-2">
                <div className="w-2 h-2 bg-green-400 rounded-full market-pulse"></div>
                Market Indices
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {marketIndices.map((index) => (
                <div key={index.name} className="flex justify-between items-center data-stream bg-accent/20 rounded-lg p-3 hover:bg-accent/40 transition-all cursor-pointer">
                  <div>
                    <div className="text-xs font-medium">{index.name}</div>
                    <div className="text-xs text-muted-foreground">{index.points}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-bold">{index.value}</div>
                    <div className={`text-xs font-semibold ${index.trend === 'up' ? 'price-up' : 'price-down'}`}>
                      {index.change}
                    </div>
                  </div>
                </div>
              ))}
              
              <div className="mt-4 pt-3 border-t border-border/30">
                <div className="grid grid-cols-2 gap-3 text-xs">
                  <div className="bg-green-500/10 rounded-lg p-2">
                    <div className="text-green-400 font-medium">VIX</div>
                    <div className="price-down">18.3 (-0.8)</div>
                  </div>
                  <div className="bg-blue-500/10 rounded-lg p-2">
                    <div className="text-blue-400 font-medium">Fear & Greed</div>
                    <div className="text-orange-400">62 (Greed)</div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Market Temperature */}
          <Card className="trading-card">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm flex items-center gap-2">
                🌡️ Market Temperature
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <div className="space-y-2">
                {[
                  { label: 'Sector Leader', value: 'Technology', color: 'price-up' },
                  { label: 'Put/Call Ratio', value: '0.87', color: 'price-neutral' },
                  { label: 'Options Flow', value: 'Bullish', color: 'text-orange-400' },
                ].map((item) => (
                  <div key={item.label} className="flex justify-between text-xs data-stream">
                    <span>{item.label}</span>
                    <span className={item.color}>{item.value}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </>
      )}

      {activeTab === 'news' && (
        <Card className="trading-card">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm flex items-center gap-2">
              ⚡ Breaking News
              <Badge variant="destructive" className="text-xs">Live</Badge>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {breakingNews.map((news, index) => (
              <div 
                key={index} 
                className={`p-3 rounded-lg text-xs ${news.impact}-impact hover:scale-[1.02] transition-all cursor-pointer`}
              >
                <div className="flex items-start gap-2">
                  {news.isBreaking && <Zap className="w-3 h-3 text-orange-500 flex-shrink-0 mt-0.5" />}
                  <div className="flex-1">
                    <div className="font-medium leading-tight">{news.headline}</div>
                    <div className="flex items-center gap-2 mt-2 text-muted-foreground">
                      <Clock className="w-3 h-3" />
                      <span>{news.time}</span>
                      <Badge variant="outline" className="text-xs uppercase ml-auto">
                        {news.impact}
                      </Badge>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {activeTab === 'movers' && (
        <Card className="trading-card">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm flex items-center gap-2">
              📊 Today's Movers
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <div className="text-xs font-medium mb-3 text-green-400 flex items-center gap-2">
                  <TrendingUp className="w-3 h-3" />
                  Top Gainers
                </div>
                <div className="space-y-2">
                  {topMovers.gainers.slice(0, 5).map((stock) => (
                    <div key={stock.symbol} className="flex justify-between items-center text-xs data-stream bg-green-500/5 rounded-lg p-2 hover:bg-green-500/10">
                      <div>
                        <div className="font-medium">{stock.symbol}</div>
                        <div className="text-muted-foreground text-[10px]">Vol: {stock.volume}</div>
                      </div>
                      <div className="text-right">
                        <div className="price-up font-semibold">{stock.change}</div>
                        <div className="text-muted-foreground">{stock.price}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <div className="text-xs font-medium mb-3 text-red-400 flex items-center gap-2">
                  <TrendingDown className="w-3 h-3" />
                  Top Losers
                </div>
                <div className="space-y-2">
                  {topMovers.losers.slice(0, 5).map((stock) => (
                    <div key={stock.symbol} className="flex justify-between items-center text-xs data-stream bg-red-500/5 rounded-lg p-2 hover:bg-red-500/10">
                      <div>
                        <div className="font-medium">{stock.symbol}</div>
                        <div className="text-muted-foreground text-[10px]">Vol: {stock.volume}</div>
                      </div>
                      <div className="text-right">
                        <div className="price-down font-semibold">{stock.change}</div>
                        <div className="text-muted-foreground">{stock.price}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Quick Actions */}
      <div className="grid grid-cols-2 gap-2 pt-2">
        <Button variant="outline" size="sm" className="text-xs h-8">
          <Eye className="w-3 h-3 mr-1" />
          Watchlist
        </Button>
        <Button variant="outline" size="sm" className="text-xs h-8">
          <AlertTriangle className="w-3 h-3 mr-1" />
          Alerts
        </Button>
      </div>
    </div>
  );
};

export default MarketSidebar;
