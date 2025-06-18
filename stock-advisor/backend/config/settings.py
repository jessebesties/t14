import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # # API Keys
    # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    # HF_TOKEN = os.getenv("HF_TOKEN", "")
    
    # Model settings
    LLM_MODEL = "microsoft/DialoGPT-small"  # Smaller model for faster inference
    
    # API settings
    HOST = "0.0.0.0"
    PORT = 8000
    
    # Data refresh intervals (in seconds)
    NEWS_REFRESH_INTERVAL = 300  # 5 minutes
    PRICE_REFRESH_INTERVAL = 60   # 1 minute

settings = Settings()