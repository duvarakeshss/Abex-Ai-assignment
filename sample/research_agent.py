import os
import requests
import json
import time
from serpapi import GoogleSearch
from newspaper import Article

# Load SerpAPI key from environment variable
SERPAPI_KEY = os.getenv("SERP_API_KEY")
if not SERPAPI_KEY:
    raise ValueError("SerpAPI API key not found. Set it in your environment variables.")

# Topics to search for
TOPICS = ["AI in HR", "Remote Work Policies", "HR Tech Trends"]

# Function to fetch Google News results using SerpAPI
def fetch_news(topic):
    search_params = {
        "q": topic,
        "tbm": "nws",
        "api_key": SERPAPI_KEY,
        "num": 5,  # Fetch 5 articles per topic
    }
    
    search = GoogleSearch(search_params)
    results = search.get_dict().get("news_results", [])
    
    articles = []
    for result in results:
        title = result.get("title")
        link = result.get("link")
        if title and link:
            articles.append({"title": title, "link": link})
    
    return articles

# Function to extract full content from an article
def extract_full_content(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text[:3000]  # Limit to 3000 characters for readability
    except Exception as e:
        return None

# Main function
def main():
    all_data = []

    for topic in TOPICS:
        topic_data = {"topic": topic, "articles": []}
        articles = fetch_news(topic)
        
        for article in articles:
            content = extract_full_content(article["link"])
            topic_data["articles"].append({
                "title": article["title"],
                "link": article["link"],
                "content": content if content else "Content not available"
            })
            
            # Delay to avoid getting blocked
            time.sleep(2)
        
        all_data.append(topic_data)

    # Convert to JSON and print output
    json_output = json.dumps(all_data, indent=4, ensure_ascii=False)
    print(json_output)

if __name__ == "__main__":
    main()
