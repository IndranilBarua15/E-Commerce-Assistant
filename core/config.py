import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ===============================
# REQUIRED API KEYS
# ===============================

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# ===============================
# OPTIONAL (LangSmith / Debug)
# ===============================

LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "ShopSmart-AI")

# ===============================
# VALIDATION
# ===============================

if not GOOGLE_API_KEY:
    raise ValueError(
        "Missing GOOGLE_API_KEY. Please add it to your .env file."
    )

if not SERPER_API_KEY:
    raise ValueError(
        "Missing SERPER_API_KEY. Please add it to your .env file."
    )