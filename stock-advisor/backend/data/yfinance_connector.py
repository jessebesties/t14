import yfinance as yf
import pathway as pw
import time
from typing import List, Dict, Any
import pandas as pd
import re

class YFinanceConnector:
    def __init__(self):
        self.cache = {}
        self.last_fetch = {}
    
    def enhanced_sentiment_analysis(self, title: str, summary: str) -> Dict[str, Any]:
        """Enhanced sentiment analysis focused on financial news"""
        
        # Combine title and summary, giving title more weight
        text = f"{title} {title} {summary}".lower()  # Title counted twice for emphasis
        
        # Financial-specific sentiment keywords with weights
        strong_positive = {
            'beats': 3, 'exceeds': 3, 'surge': 3, 'soars': 3, 'breakthrough': 3,
            'record': 2, 'upgrade': 2, 'bullish': 2, 'rally': 2, 'gains': 2,
            'profit': 2, 'growth': 2, 'strong': 2, 'outperforms': 3, 'acquisition': 2
        }
        
        moderate_positive = {
            'up': 1, 'rise': 1, 'positive': 1, 'good': 1, 'increase': 1,
            'buy': 1, 'optimistic': 1, 'confidence': 1, 'expansion': 1, 'deal': 1
        }
        
        strong_negative = {
            'plunges': -3, 'crashes': -3, 'collapses': -3, 'bankruptcy': -3, 'scandal': -3,
            'downgrade': -2, 'bearish': -2, 'losses': -2, 'decline': -2, 'miss': -2,
            'disappointing': -2, 'weak': -2, 'concern': -2, 'investigation': -2
        }
        
        moderate_negative = {
            'down': -1, 'fall': -1, 'drop': -1, 'negative': -1, 'sell': -1,
            'risk': -1, 'challenge': -1, 'pressure': -1, 'uncertainty': -1
        }
        
        # Calculate weighted sentiment score
        score = 0
        word_matches = 0
        
        for word, weight in {**strong_positive, **moderate_positive}.items():
            count = text.count(word)
            score += count * weight
            word_matches += count
            
        for word, weight in {**strong_negative, **moderate_negative}.items():
            count = text.count(word)
            score += count * weight  # weight is already negative
            word_matches += count
        
        # Normalize score
        if word_matches > 0:
            normalized_score = score / (word_matches + 5)  # +5 to prevent extreme scores
        else:
            normalized_score = 0
        
        # Determine sentiment strength and confidence
        if abs(normalized_score) > 0.3:
            confidence = min(0.9, abs(normalized_score))
            strength = "strong"
        elif abs(normalized_score) > 0.1:
            confidence = min(0.7, abs(normalized_score) + 0.2)
            strength = "moderate"
        else:
            confidence = 0.3
            strength = "weak"
        
        # Determine sentiment direction
        if normalized_score > 0.05:
            sentiment = "positive"
        elif normalized_score < -0.05:
            sentiment = "negative"
        else:
            sentiment = "neutral"
            
        return {
            "sentiment": sentiment,
            "score": normalized_score,
            "confidence": confidence,
            "strength": strength,
            "word_matches": word_matches,
            "raw_score": score
        }
    
    def get_stock_news(self, ticker: str, max_articles: int = 10) -> List[Dict[str, Any]]:
        """Fetch news with enhanced sentiment analysis"""
        try:
            stock = yf.Ticker(ticker)
            news = stock.news[:max_articles]
            
            processed_news = []
            for article in news:
                title = article.get('title', '')
                summary = article.get('summary', '')
                
                sentiment_data = self.enhanced_sentiment_analysis(title, summary)
                
                processed_news.append({
                    'ticker': ticker,
                    'title': title,
                    'summary': summary,
                    'link': article.get('link', ''),
                    'publish_time': article.get('providerPublishTime', 0),
                    'sentiment': sentiment_data['sentiment'],
                    'sentiment_score': sentiment_data['score'],
                    'sentiment_confidence': sentiment_data['confidence'],
                    'sentiment_strength': sentiment_data['strength'],
                    'word_matches': sentiment_data['word_matches']
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
        """Create a Pathway stream for news data with enhanced sentiment"""
        def news_generator():
            while True:
                for ticker in tickers:
                    news_data = self.get_stock_news(ticker)
                    for article in news_data:
                        yield article
                time.sleep(60)
        
        return pw.io.python.read(
            news_generator(),
            schema=pw.Schema.from_types(
                ticker=str,
                title=str,
                summary=str,
                link=str,
                publish_time=int,
                sentiment=str,
                sentiment_score=float,
                sentiment_confidence=float,
                sentiment_strength=str,
                word_matches=int
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
                time.sleep(30)
        
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