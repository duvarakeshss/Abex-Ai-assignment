import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

# Load environment variables from .env file (if using .env)
load_dotenv()

# Get API key from environment variable
SERP_API_KEY = os.getenv("SERP_API_KEY")

if not SERP_API_KEY:
    raise ValueError("Missing SERPAPI_API_KEY. Set it in your environment variables or .env file.")

# Trending HR topics
trending_topics = [
    "AI in HR",
    "Remote Work Policies",
    "Employee Well-being",
    "HR Tech Trends",
    "Diversity & Inclusion"
]

# Function to fetch news articles for a given topic
def fetch_news(topic):
    params = {
        "q": topic,
        "tbm": "nws",  # News search
        "api_key": SERP_API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    
    articles = results.get("news_results", [])
    
    if not articles:
        return "No articles found."
    
    top_article = articles[0]  # Fetching the first result
    return f"Title: {top_article['title']}\nSource: {top_article['source']}\nLink: {top_article['link']}\nSnippet: {top_article.get('snippet', 'No summary available')}"

# Fetch and display news for each topic
for topic in trending_topics:
    print(f"### {topic} ###")
    print(fetch_news(topic))
    print("\n" + "-"*50 + "\n")
