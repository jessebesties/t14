import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pathway as pw
from data.yfinance_connector import YFinanceConnector
from pipeline.llm_analyzer import StockLLMAnalyzer
import time

class StockETLPipeline:
    def __init__(self, tickers):
        self.tickers = tickers
        self.yfinance_connector = YFinanceConnector()
        self.llm_analyzer = StockLLMAnalyzer()
        
    def run_pipeline(self):
        """Run the complete ETL pipeline"""
        
        # Extract: Create data streams
        print("Setting up data streams...")
        
        # News stream
        news_stream = self.yfinance_connector.create_pathway_news_stream(self.tickers)
        
        # Price stream  
        price_stream = self.yfinance_connector.create_pathway_price_stream(self.tickers)
        
        # Transform: Join and process data
        print("Setting up data transformations...")
        
        # Join news and price data on ticker
        combined_data = news_stream.join(
            price_stream, 
            pw.left.ticker == pw.right.ticker
        ).select(
            ticker=pw.left.ticker,
            title=pw.left.title,
            summary=pw.left.summary,
            current_price=pw.right.current_price,
            price_change_pct=pw.right.price_change_pct,
            volume=pw.right.volume,
            high_5d=pw.right.high_5d,
            low_5d=pw.right.low_5d,
            timestamp=pw.right.timestamp
        )
        
        # Load: Generate analysis
        print("Setting up LLM analysis...")
        
        analysis_results = self.llm_analyzer.analyze_stock_data(combined_data)
        
        # Create final output
        final_output = analysis_results.select(
            ticker=pw.this.ticker,
            recommendation=pw.this.analysis,
            timestamp=pw.cast(int, time.time())
        )
        
        return final_output
    
    def get_latest_analysis(self, ticker):
        """Get the latest analysis for a specific ticker"""
        try:
            # Get fresh data
            price_data = self.yfinance_connector.get_stock_price_data(ticker)
            news_data = self.yfinance_connector.get_stock_news(ticker, 5)
            
            if not price_data:
                return {"error": "Unable to fetch price data"}
            
            # Create simple analysis prompt
            news_summary = " | ".join([article['title'] for article in news_data[:3]])
            
            prompt = f"""
Analyze {ticker} stock:

Price: ${price_data['current_price']:.2f} ({price_data['price_change_pct']:.2f}%)
Recent news: {news_summary}

Give a BUY/SELL/HOLD recommendation with simple reasoning in under 100 words.
"""
            
            # For now, return a mock analysis (replace with actual LLM call)
            if price_data['price_change_pct'] > 2:
                recommendation = "BUY"
                reasoning = f"{ticker} is up {price_data['price_change_pct']:.1f}% with positive momentum."
            elif price_data['price_change_pct'] < -2:
                recommendation = "SELL"  
                reasoning = f"{ticker} is down {price_data['price_change_pct']:.1f}% showing weakness."
            else:
                recommendation = "HOLD"
                reasoning = f"{ticker} showing stable movement at ${price_data['current_price']:.2f}."
            
            return {
                "ticker": ticker,
                "recommendation": recommendation,
                "reasoning": reasoning,
                "confidence": "Medium",
                "current_price": price_data['current_price'],
                "price_change_pct": price_data['price_change_pct'],
                "timestamp": int(time.time())
            }
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}