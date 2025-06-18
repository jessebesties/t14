import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
import uvicorn
from api.server import app
from config.settings import settings

def main():
    """Main entry point for the application"""
    print("Starting Stock Advisor Backend...")
    print(f"Server will run on http://{settings.HOST}:{settings.PORT}")
    
    uvicorn.run(
        "api.server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()