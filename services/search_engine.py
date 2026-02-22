import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def get_live_products(query, limit=10):
    if not SERPER_API_KEY:
        raise ValueError("SERPER_API_KEY missing in .env")

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "q": query,
        "gl": "in",
        "hl": "en",
        "num": limit
    }

    response = requests.post(
        "https://google.serper.dev/shopping",
        headers=headers,
        json=payload,
        timeout=15
    )

    response.raise_for_status()
    data = response.json()

    return {"shopping": data.get("shopping", [])[:limit]}
