import yfinance as yf
import pathway as pw
import time
from typing import List, Dict, Any
import pandas as pd

class YFinanceConnector:
    def __init__(self):
        self.cache = {}
        self.last_fetch = {}
    
    def get_stock_news(self, ticker: str, max_articles: int = 10) -> List[Dict[str, Any]]:
        """Fetch news for a given ticker"""
        try:
            stock = yf.Ticker(ticker)
            news = stock.news[:max_articles]
            
            processed_news = []
            for article in news:
                processed_news.append({
                    'ticker': ticker,
                    'title': article.get('title', ''),
                    'summary': article.get('summary', ''),
                    'link': article.get('link', ''),
                    'publish_time': article.get('providerPublishTime', 0),
                    'sentiment': 'neutral'  # Will be analyzed by LLM
                })
            
            return processed_news
            
        except Exception as e:
            print(f"Error fetching news for {ticker}: {e}")
            return []
    
    def get_stock_price_data(self, ticker: str, period: str = "5d") -> Dict[str, Any]:
        """Fetch price data for a given ticker"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            
            if hist.empty:
                return {}
            
            current_price = hist['Close'].iloc[-1]
            prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            price_change = current_price - prev_price
            price_change_pct = (price_change / prev_price) * 100
            
            return {
                'ticker': ticker,
                'current_price': float(current_price),
                'previous_price': float(prev_price),
                'price_change': float(price_change),
                'price_change_pct': float(price_change_pct),
                'volume': int(hist['Volume'].iloc[-1]),
                'high_5d': float(hist['High'].max()),
                'low_5d': float(hist['Low'].min()),
                'timestamp': int(time.time())
            }
            
        except Exception as e:
            print(f"Error fetching price data for {ticker}: {e}")
            return {}
    
    def create_pathway_news_stream(self, tickers: List[str]):
        """Create a Pathway stream for news data"""
        def news_generator():
            while True:
                for ticker in tickers:
                    news_data = self.get_stock_news(ticker)
                    for article in news_data:
                        yield article
                time.sleep(60)  # Wait 1 minute between updates
        
        return pw.io.python.read(
            news_generator(),
            schema=pw.Schema.from_types(
                ticker=str,
                title=str,
                summary=str,
                link=str,
                publish_time=int,
                sentiment=str
            )
        )
    
    def create_pathway_price_stream(self, tickers: List[str]):
        """Create a Pathway stream for price data"""
        def price_generator():
            while True:
                for ticker in tickers:
                    price_data = self.get_stock_price_data(ticker)
                    if price_data:
                        yield price_data
                time.sleep(30)  # Wait 30 seconds between updates
        
        return pw.io.python.read(
            price_generator(),
            schema=pw.Schema.from_types(
                ticker=str,
                current_price=float,
                previous_price=float,
                price_change=float,
                price_change_pct=float,
                volume=int,
                high_5d=float,
                low_5d=float,
                timestamp=int
            )
        )