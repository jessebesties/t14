import requests
import feedparser
from typing import List, Dict, Any
import time

class AlternativeNewsFetcher:
    def __init__(self):
        self.base_urls = {
            "yahoo": "https://feeds.finance.yahoo.com/rss/2.0/headline?s={}&region=US&lang=en-US",
            "google": "https://news.google.com/rss/search?q={}&hl=en-US&gl=US&ceid=US:en"
        }
    
    def get_stock_news_from_feeds(self, ticker: str, max_articles: int = 10) -> List[Dict[str, Any]]:
        """Get news from RSS feeds as backup"""
        all_articles = []
        
        for source, url_template in self.base_urls.items():
            try:
                url = url_template.format(ticker)
                print(f"Fetching from {source}: {url}")
                
                feed = feedparser.parse(url)
                
                for entry in feed.entries[:max_articles//2]:  # Split between sources
                    article = {
                        'ticker': ticker,
                        'title': entry.get('title', ''),
                        'summary': entry.get('summary', entry.get('description', '')),
                        'link': entry.get('link', ''),
                        'publish_time': int(time.mktime(entry.get('published_parsed', time.gmtime()))),
                        'source': source
                    }
                    all_articles.append(article)
                    
            except Exception as e:
                print(f"Error fetching from {source}: {e}")
                
        return all_articles[:max_articles]
    
    def simple_web_search_news(self, ticker: str) -> List[Dict[str, Any]]:
        """Fallback method using simple web search"""
        # This is a very basic fallback - you might want to use a proper news API
        mock_news = [
            {
                'ticker': ticker,
                'title': f'{ticker} stock analysis shows mixed signals in current market',
                'summary': f'Recent trading activity for {ticker} indicates varied investor sentiment with price movements reflecting broader market conditions.',
                'link': '',
                'publish_time': int(time.time()),
                'source': 'mock'
            },
            {
                'ticker': ticker,
                'title': f'Market watch: {ticker} continues to track with sector trends',
                'summary': f'Financial analysts note that {ticker} performance aligns with industry patterns amid ongoing market volatility.',
                'link': '',
                'publish_time': int(time.time()) - 3600,
                'source': 'mock'
            }
        ]
        return mock_news