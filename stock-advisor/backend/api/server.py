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
                "response": "Hey there! I'm your AI market analyst, and I'd love to help you understand what's happening in the markets. I can dive deep into any stock you're curious about - just mention a ticker symbol like AAPL for Apple, TSLA for Tesla, or NVDA for Nvidia. I'll analyze the latest price movements, dig through recent news, and give you my honest take on whether it might be a good time to buy, sell, or hold. What stock has caught your attention lately?",
                "data": None
            }
        
        print(f"Analyzing ticker: {ticker}")
        
        # Get analysis
        analysis = pipeline.get_latest_analysis(ticker)
        
        if "error" in analysis:
            return {
                "success": False,
                "response": f"I'm having some trouble pulling the latest data for {ticker} right now. This sometimes happens when markets are closed or if there's a temporary glitch with the data feeds. Give me a moment and try asking about {ticker} again, or feel free to ask about a different stock in the meantime.",
                "data": None
            }
        
        # Create natural, conversational response
        company_names = {
            "AAPL": "Apple", "MSFT": "Microsoft", "GOOGL": "Google", 
            "TSLA": "Tesla", "NVDA": "Nvidia", "AMZN": "Amazon",
            "META": "Meta", "NFLX": "Netflix", "AMD": "AMD", "INTC": "Intel"
        }
        
        company_name = company_names.get(ticker, ticker)
        
        # Start with current situation
        price_change_desc = ""
        if analysis['price_change_pct'] > 2:
            price_change_desc = f"having a strong day, up {analysis['price_change_pct']:.1f}%"
        elif analysis['price_change_pct'] > 0.5:
            price_change_desc = f"trending upward, gaining {analysis['price_change_pct']:.1f}%"
        elif analysis['price_change_pct'] < -2:
            price_change_desc = f"under pressure today, down {analysis['price_change_pct']:.1f}%"
        elif analysis['price_change_pct'] < -0.5:
            price_change_desc = f"dipping slightly, down {analysis['price_change_pct']:.1f}%"
        else:
            price_change_desc = f"trading relatively flat, {analysis['price_change_pct']:+.1f}%"
        
        # News sentiment context
        positive_news = analysis.get('positive_news_count', 0)
        negative_news = analysis.get('negative_news_count', 0)
        total_news = analysis.get('total_news_count', 0)
        
        news_context = ""
        if total_news > 0:
            if positive_news > negative_news:
                news_context = f"The news flow has been quite positive lately, with {positive_news} upbeat articles versus {negative_news} negative ones. "
            elif negative_news > positive_news:
                news_context = f"There's been some concerning news recently, with {negative_news} negative articles outweighing {positive_news} positive ones. "
            else:
                news_context = f"The news has been mixed, with roughly equal positive and negative coverage across {total_news} recent articles. "
        
        # Headlines context
        headlines = analysis.get('top_headlines', [])
        headline_context = ""
        if headlines:
            headline_context = f"Recent headlines include stories like '{headlines[0][:60]}...'" if len(headlines[0]) > 60 else f"Recent headlines include '{headlines[0]}'"
            if len(headlines) > 1:
                headline_context += f" and '{headlines[1][:50]}...'" if len(headlines[1]) > 50 else f" and '{headlines[1]}'"
            headline_context += ". "
        
        # Confidence explanation
        confidence_explanation = ""
        if analysis['confidence'] == "High":
            confidence_explanation = "I'm quite confident in this assessment because the signals from both price action and news sentiment are aligning well."
        elif analysis['confidence'] == "Medium":
            confidence_explanation = "I'd say I'm moderately confident here - there are some good indicators, but I'd keep an eye on how things develop."
        else:
            confidence_explanation = "I'm being cautious with this one since the signals are a bit mixed or unclear right now."
        
        # Recommendation with natural language
        recommendation_text = ""
        if analysis['recommendation'] == "BUY":
            recommendation_text = "Based on what I'm seeing, I think this could be a good buying opportunity. "
        elif analysis['recommendation'] == "SELL":
            recommendation_text = "Honestly, I'd be inclined to sell or avoid this one for now. "
        else:
            recommendation_text = "I think the best move here is to hold tight and wait for clearer signals. "
        
        # Construct the full response
        response = f"Looking at {company_name} right now, it's {price_change_desc} to ${analysis['current_price']:.2f}. {news_context}{headline_context}{recommendation_text}{analysis['reasoning']} {confidence_explanation}"
        
        # Add a personal touch
        if analysis['recommendation'] == "BUY":
            response += " Of course, this is just my analysis based on current data - always do your own research and consider your risk tolerance!"
        elif analysis['recommendation'] == "SELL":
            response += " That said, markets can be unpredictable, so this is just my take based on current information."
        else:
            response += " Sometimes patience is the best strategy in investing."
        
        return {
            "success": True,
            "response": response,
            "data": analysis
        }
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return {
            "success": False,
            "response": "Oops, I ran into a technical hiccup while analyzing that for you. These things happen sometimes with live market data. Mind giving it another shot in a moment?",
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