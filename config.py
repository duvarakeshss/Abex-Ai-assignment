import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Config:
    SERP_API_KEY = os.getenv("SERP_API_KEY")
    SERP_API_URL = "https://serpapi.com/search"
    DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL")
    SEARCH_QUERY = os.getenv("SEARCH_QUERY")
    MAX_TOKENS = 3000
    TEMPERATURE = 0.7
    TOP_P = 0.9


if not Config.SERP_API_KEY or not Config.DEEPSEEK_API_URL:
    raise ValueError("Missing API keys. Check your .env file.")
