import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") 
SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

# DEV MODE SWITCH
# Set to False to use Real Gemini + SerpAPI
USE_MOCK_DATA = False 

if not GOOGLE_API_KEY:
    raise ValueError("Missing Google API Key! Please add GOOGLE_API_KEY to your .env file.")