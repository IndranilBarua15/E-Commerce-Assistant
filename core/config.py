import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

# DEV MODE SWITCH
# Set to True to save API credits while testing UI
# Set to False for the final presentation
USE_MOCK_DATA = False 

if not HUGGINGFACE_TOKEN:
    raise ValueError("Missing Hugging Face Token! Check .env file.")