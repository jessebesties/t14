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
    allow_origins=["*"],  # Configure this properly for production
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
            # Remove common punctuation
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
                "response": "Please mention a stock ticker (like AAPL, MSFT, GOOGL, TSLA, NVDA) or company name and I'll analyze it for you!",
                "data": None
            }
        
        print(f"Analyzing ticker: {ticker}")  # Debug log
        
        # Get analysis
        analysis = pipeline.get_latest_analysis(ticker)
        
        if "error" in analysis:
            return {
                "success": False,
                "response": f"Sorry, I couldn't analyze {ticker} right now. Please try again later.",
                "data": None
            }
        
        # Format response for chat
        response = f"""📊 **{ticker} Analysis**

💰 **Current Price:** ${analysis['current_price']:.2f} ({analysis['price_change_pct']:+.1f}%)

🎯 **Recommendation:** {analysis['recommendation']}

📝 **Reasoning:** {analysis['reasoning']}

🎚️ **Confidence:** {analysis['confidence']}

_Analysis updated at {analysis['timestamp']}_"""
        
        return {
            "success": True,
            "response": response.strip(),
            "data": analysis
        }
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")  # Debug log
        return {
            "success": False,
            "response": "Sorry, I encountered an error while processing your request.",
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