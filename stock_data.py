import yfinance as yf
import pandas as pd
import json
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup

# Add rate limiting and better headers for web scraping
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

def scrape_yahoo_content(url, delay=2):
    """Scrape content from Yahoo Finance URLs with rate limiting"""
    try:
        time.sleep(delay)  # Rate limiting
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract text content (adjust selectors as needed)
            content = soup.get_text(strip=True)
            return content
        else:
            return f"Error: {response.status_code} - {response.text[:100]}"
    except Exception as e:
        return f"Scraping error: {str(e)}"

def get_comprehensive_stock_data(symbol):
    ticker = yf.Ticker(symbol)
    
    # Get yfinance data
    info = ticker.info
    hist = ticker.history(period="5d")
    news = ticker.news
    
    # Prepare comprehensive data structure
    stock_data = {
        'symbol': symbol,
        'yfinance_data': {
            'current_price': float(hist['Close'].iloc[-1]),
            'company_name': info.get('longName', 'N/A'),
            'market_cap': info.get('marketCap', 'N/A'),
            'pe_ratio': info.get('trailingPE', 'N/A'),
            'volume': int(hist['Volume'].iloc[-1]) if not hist['Volume'].empty else 0,
            'day_high': float(hist['High'].iloc[-1]),
            'day_low': float(hist['Low'].iloc[-1]),
        },
        'news_data': {
            'yfinance_news': [
                {
                    'title': article.get('title', ''),
                    'link': article.get('link', ''),
                    'published': article.get('providerPublishTime', ''),
                    'summary': article.get('summary', '')
                } for article in (news[:5] if news else [])
            ],
            'scraped_content': []
        },
        'timestamp': datetime.now().isoformat()
    }
    
    # Scrape content from news URLs (with rate limiting)
    if news:
        for i, article in enumerate(news[:3]):  # Limit to 3 to avoid rate limiting
            url = article.get('link', '')
            if url:
                print(f"Scraping content from: {url}")
                scraped_text = scrape_yahoo_content(url, delay=3)  # 3 second delay
                stock_data['news_data']['scraped_content'].append({
                    'url': url,
                    'title': article.get('title', ''),
                    'scraped_text': scraped_text[:1000] + '...' if len(scraped_text) > 1000 else scraped_text  # Truncate if too long
                })
    
    return stock_data

# Get comprehensive data for stocks
symbols = ['MSFT', 'AAPL', 'GOOGL']
comprehensive_stock_data = {}

for symbol in symbols:
    try:
        print(f"\nProcessing {symbol}...")
        data = get_comprehensive_stock_data(symbol)
        comprehensive_stock_data[symbol] = data
        print(f"✓ Collected comprehensive data for {symbol}")
    except Exception as e:
        print(f"✗ Error collecting data for {symbol}: {e}")

# Write to JSON file
output_file = '/Users/adi/Desktop/t14/comprehensive_stock_data.json'
with open(output_file, 'w') as f:
    json.dump(comprehensive_stock_data, f, indent=2, default=str)

print(f"\nComprehensive stock data saved to: {output_file}")
print(f"Total stocks processed: {len(comprehensive_stock_data)}")