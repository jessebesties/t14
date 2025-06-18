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
    
    def calculate_news_based_confidence(self, price_change_pct, news_data):
        """Calculate confidence based primarily on news sentiment analysis"""
        
        if not news_data:
            return "Low", "No news data available for analysis"
        
        # Extract sentiment metrics
        sentiment_scores = [article['sentiment_score'] for article in news_data]
        sentiment_confidences = [article['sentiment_confidence'] for article in news_data]
        sentiment_strengths = [article['sentiment_strength'] for article in news_data]
        
        # Calculate news consensus
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
        avg_confidence = sum(sentiment_confidences) / len(sentiment_confidences)
        
        # Count strong vs weak sentiment signals
        strong_signals = len([s for s in sentiment_strengths if s == "strong"])
        moderate_signals = len([s for s in sentiment_strengths if s == "moderate"])
        weak_signals = len([s for s in sentiment_strengths if s == "weak"])
        
        # Check alignment between news sentiment and price movement
        price_direction = "positive" if price_change_pct > 1 else "negative" if price_change_pct < -1 else "neutral"
        news_direction = "positive" if avg_sentiment > 0.05 else "negative" if avg_sentiment < -0.05 else "neutral"
        
        alignment = price_direction == news_direction or (price_direction == "neutral" and news_direction == "neutral")
        
        # Calculate base confidence from news quality
        news_quality_score = (strong_signals * 0.8 + moderate_signals * 0.5 + weak_signals * 0.2) / len(news_data)
        sentiment_certainty = avg_confidence
        
        # Alignment bonus/penalty
        alignment_factor = 1.2 if alignment else 0.7
        
        # Final confidence calculation
        final_confidence = (news_quality_score * 0.6 + sentiment_certainty * 0.4) * alignment_factor
        
        # Generate reasoning
        reasoning_parts = []
        reasoning_parts.append(f"{len(news_data)} news articles analyzed")
        reasoning_parts.append(f"{strong_signals} strong, {moderate_signals} moderate sentiment signals")
        
        if alignment:
            reasoning_parts.append(f"News sentiment aligns with price movement ({news_direction})")
        else:
            reasoning_parts.append(f"News sentiment conflicts with price movement (news: {news_direction}, price: {price_direction})")
        
        reasoning = ". ".join(reasoning_parts)
        
        # Convert to confidence levels
        if final_confidence >= 0.7:
            return "High", reasoning
        elif final_confidence >= 0.4:
            return "Medium", reasoning
        else:
            return "Low", reasoning
    
    def get_latest_analysis(self, ticker):
        """Get analysis with news-driven confidence"""
        try:
            # Get fresh data
            price_data = self.yfinance_connector.get_stock_price_data(ticker)
            news_data = self.yfinance_connector.get_stock_news(ticker, 8)  # More articles for better analysis
            
            if not price_data:
                return {"error": "Unable to fetch price data"}
            
            # Calculate news-based confidence
            confidence, confidence_reasoning = self.calculate_news_based_confidence(
                price_data['price_change_pct'], 
                news_data
            )
            
            # Enhanced recommendation logic based on news sentiment
            if not news_data:
                recommendation = "HOLD"
                reasoning = f"There isn't much news flow around {ticker} right now, which makes it tricky to get a strong read on market sentiment. With the stock trading at ${price_data['current_price']:.2f}, I'd suggest waiting for more information before making any big moves."
            else:
                # Calculate news metrics
                sentiment_scores = [article['sentiment_score'] for article in news_data]
                avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
                positive_count = len([s for s in sentiment_scores if s > 0.05])
                negative_count = len([s for s in sentiment_scores if s < -0.05])
                strong_sentiment_count = len([article for article in news_data if article['sentiment_strength'] == 'strong'])
                
                # Decision logic based on news sentiment
                if avg_sentiment > 0.1 and positive_count >= negative_count:
                    recommendation = "BUY"
                    reasoning = f"The sentiment around {ticker} is really encouraging right now. I'm seeing {positive_count} positive stories compared to just {negative_count} negative ones, which suggests the market mood is quite optimistic. The overall sentiment score of {avg_sentiment:.2f} reinforces this bullish outlook."
                    
                elif avg_sentiment < -0.1 and negative_count > positive_count:
                    recommendation = "SELL"
                    reasoning = f"I'm seeing some concerning patterns in the news coverage for {ticker}. With {negative_count} negative articles outweighing {positive_count} positive ones, and an overall sentiment score of {avg_sentiment:.2f}, it feels like there might be some headwinds ahead."
                    
                elif strong_sentiment_count >= 2:
                    if avg_sentiment > 0:
                        recommendation = "BUY"
                        reasoning = f"What's interesting here is that I'm picking up {strong_sentiment_count} really strong sentiment signals in the news, which tends to be a good indicator. Even though the overall picture might be mixed, these strong positive signals could mean something big is brewing."
                    else:
                        recommendation = "HOLD"
                        reasoning = f"There are {strong_sentiment_count} strong sentiment signals in the news, but they're pointing in different directions. When I see this kind of conflicting but intense coverage, I usually think it's better to wait and see how things settle out."
                    
                else:
                    recommendation = "HOLD"
                    reasoning = f"The news sentiment is pretty balanced right now - {positive_count} positive articles, {negative_count} negative ones. When things are this evenly split, I typically recommend taking a wait-and-see approach rather than making any hasty decisions."
            
            # Get sample news headlines for context
            top_headlines = [article['title'] for article in news_data[:3]]
            
            return {
                "ticker": ticker,
                "recommendation": recommendation,
                "reasoning": reasoning,
                "confidence": confidence,
                "confidence_reasoning": confidence_reasoning,
                "current_price": price_data['current_price'],
                "price_change_pct": price_data['price_change_pct'],
                "avg_sentiment_score": sum([article['sentiment_score'] for article in news_data]) / len(news_data) if news_data else 0,
                "positive_news_count": len([article for article in news_data if article['sentiment'] == 'positive']),
                "negative_news_count": len([article for article in news_data if article['sentiment'] == 'negative']),
                "neutral_news_count": len([article for article in news_data if article['sentiment'] == 'neutral']),
                "strong_sentiment_signals": len([article for article in news_data if article['sentiment_strength'] == 'strong']),
                "total_news_count": len(news_data),
                "top_headlines": top_headlines,
                "timestamp": int(time.time())
            }
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
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
            sentiment=pw.left.sentiment,
            sentiment_score=pw.left.sentiment_score,
            sentiment_confidence=pw.left.sentiment_confidence,
            sentiment_strength=pw.left.sentiment_strength,
            current_price=pw.right.current_price,
            price_change_pct=pw.right.price_change_pct,
            volume=pw.right.volume,
            timestamp=pw.right.timestamp
        )
        
        return combined_data