import yfinance as yf

def test_news_extraction():
    tickers = ["AAPL", "TSLA", "NVDA", "MSFT"]
    
    for ticker in tickers:
        print(f"\n{'='*50}")
        print(f"Testing {ticker}")
        print(f"{'='*50}")
        
        try:
            stock = yf.Ticker(ticker)
            
            # Test news
            news = stock.news
            print(f"News type: {type(news)}")
            print(f"News length: {len(news) if news else 0}")
            
            if news and len(news) > 0:
                print(f"First article keys: {news[0].keys()}")
                print(f"Title: {news[0].get('title', 'No title')}")
                print(f"Summary: {news[0].get('summary', 'No summary')[:200]}...")
            else:
                print("No news found")
                
                # Try alternative approaches
                print("Trying info...")
                info = stock.info
                print(f"Info available: {bool(info)}")
                
        except Exception as e:
            print(f"Error with {ticker}: {e}")

if __name__ == "__main__":
    test_news_extraction()