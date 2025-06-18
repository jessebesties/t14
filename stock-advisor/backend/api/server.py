import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pipeline.etl_pipeline import StockETLPipeline
from config.settings import settings
import asyncio

app = FastAPI(title="Stock Advisor API", version="1.0.0")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:5173", 
        "http://localhost:5174",  # Sometimes Vite uses this port
        "http://127.0.0.1:3000", 
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "*"  # Allow all origins for development (remove in production)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pipeline
pipeline = StockETLPipeline(["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"])

@app.get("/")
async def root():
    return {"message": "Stock Advisor API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is operational"}

@app.get("/analyze/{ticker}")
async def analyze_stock(ticker: str):
    """Get stock analysis for a specific ticker"""
    try:
        ticker = ticker.upper()
        analysis = pipeline.get_latest_analysis(ticker)
        
        if "error" in analysis:
            raise HTTPException(status_code=400, detail=analysis["error"])
        
        return {
            "success": True,
            "data": analysis,
            "message": f"Analysis completed for {ticker}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/chat")
async def chat_endpoint(request: dict):
    """Chat endpoint for frontend integration"""
    try:
        user_message = request.get("message", "").strip()
        
        # Improved ticker extraction
        words = user_message.upper().replace("?", " ").replace("!", " ").replace(",", " ").split()
        common_tickers = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "AMZN", "META", "NFLX", "AMD", "INTC"]
        
        ticker = None
        
        # Check for exact ticker matches
        for word in words:
            clean_word = word.strip(".,!?()[]")
            if clean_word in common_tickers:
                ticker = clean_word
                break
        
        # Also check for company names
        company_map = {
            "APPLE": "AAPL",
            "MICROSOFT": "MSFT", 
            "GOOGLE": "GOOGL",
            "TESLA": "TSLA",
            "NVIDIA": "NVDA",
            "AMAZON": "AMZN",
            "META": "META",
            "FACEBOOK": "META",
            "NETFLIX": "NFLX",
            "AMD": "AMD",
            "INTEL": "INTC"
        }
        
        if not ticker:
            for word in words:
                clean_word = word.strip(".,!?()[]")
                if clean_word in company_map:
                    ticker = company_map[clean_word]
                    break
        
        if not ticker:
            return {
                "success": True,
                "response": "🤖 **FinBot here!** \n\nI can analyze stocks and provide market insights. Please mention a stock ticker like:\n\n• **AAPL** (Apple)\n• **TSLA** (Tesla) \n• **NVDA** (Nvidia)\n• **MSFT** (Microsoft)\n• **GOOGL** (Google)\n\nTry asking: *\"What do you think about AAPL?\"* or *\"Analyze TSLA for me\"*",
                "data": None
            }
        
        print(f"Analyzing ticker: {ticker}")
        
        # Get analysis
        analysis = pipeline.get_latest_analysis(ticker)
        
        if "error" in analysis:
            return {
                "success": False,
                "response": f"❌ **Analysis Error**\n\nSorry, I couldn't analyze **{ticker}** right now. This could be due to:\n\n• Market is closed\n• Invalid ticker symbol\n• Data service temporarily unavailable\n\nPlease try again later or try a different stock.",
                "data": None
            }
        
        # Format response for chat - enhanced with emojis and better structure
        confidence_emoji = "🟢" if analysis['confidence'] == "High" else "🟡" if analysis['confidence'] == "Medium" else "🔴"
        recommendation_emoji = "📈" if analysis['recommendation'] == "BUY" else "📉" if analysis['recommendation'] == "SELL" else "➡️"
        sentiment_emoji = "😊" if analysis.get('avg_sentiment_score', 0) > 0.1 else "😟" if analysis.get('avg_sentiment_score', 0) < -0.1 else "😐"
        
        response = f"""📊 **{ticker} Stock Analysis**

{recommendation_emoji} **Recommendation:** {analysis['recommendation']}

💰 **Current Price:** ${analysis['current_price']:.2f} ({analysis['price_change_pct']:+.1f}%)

📝 **Reasoning:** {analysis['reasoning']}

{confidence_emoji} **Confidence:** {analysis['confidence']}

{sentiment_emoji} **News Sentiment:** {analysis.get('positive_news_count', 0)} positive, {analysis.get('negative_news_count', 0)} negative ({analysis.get('total_news_count', 0)} total articles)

📰 **Recent Headlines:**"""

        # Add top headlines if available
        headlines = analysis.get('top_headlines', [])
        for i, headline in enumerate(headlines[:2], 1):
            response += f"\n{i}. {headline[:80]}{'...' if len(headline) > 80 else ''}"

        response += f"\n\n⏰ *Analysis updated at {analysis['timestamp']} • Powered by Pathway + yfinance*"
        
        return {
            "success": True,
            "response": response.strip(),
            "data": analysis
        }
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return {
            "success": False,
            "response": "🚨 **System Error**\n\nI encountered an unexpected error while processing your request. Please try again in a moment.",
            "data": None,
            "error": str(e)
        }

if __name__ == "__main__":
    uvicorn.run(
        "api.server:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=True
    )