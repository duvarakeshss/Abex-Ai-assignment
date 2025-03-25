import os
import concurrent.futures
import requests
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import json

# Load API key from environment variable (if needed for backup search)
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Start Selenium WebDriver once and reuse
driver = uc.Chrome(headless=True)

def fetch_search_results(query):
    """Scrape Google News search results using requests."""
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=nws"
    try:
        response = requests.get(search_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        articles = []
        for item in soup.select(".SoaBEf"):
            title_tag = item.select_one(".nDgy9d")
            link_tag = item.select_one(".WlydOe")
            source_tag = item.select_one(".SVJrMe")
            date_tag = item.select_one(".LfVVr")
            
            if title_tag and link_tag:
                articles.append({
                    "title": title_tag.text,
                    "link": link_tag["href"],
                    "source": source_tag.text if source_tag else "Unknown",
                    "published_date": date_tag.text if date_tag else "Unknown"
                })
        return articles
    except Exception as e:
        print(f"Error fetching search results for {query}: {e}")
    return []

def extract_content(url):
    """Extract article content using Requests first, Selenium as fallback."""
    try:
        # Try requests first
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")
            content = "\n".join(p.text for p in paragraphs[:50])
            if content.strip():
                return content  # Return if non-empty

        # Fallback to Selenium
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        paragraphs = soup.find_all("p")
        content = "\n".join(p.text for p in paragraphs[:50])
        return content if content.strip() else "Content extraction failed."
    
    except Exception as e:
        return f"Error extracting content: {str(e)}"

def process_topic(topic):
    """Process a single topic: fetch articles, extract content."""
    articles = fetch_search_results(topic)
    extracted_data = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_article = {executor.submit(extract_content, art["link"]): art for art in articles}
        
        for future in concurrent.futures.as_completed(future_to_article):
            article = future_to_article[future]
            try:
                content = future.result()
                extracted_data.append({
                    "title": article["title"],
                    "link": article["link"],
                    "source": article["source"],
                    "published_date": article["published_date"],
                    "content": content
                })
            except Exception as e:
                print(f"Error processing {article['link']}: {e}")
    
    return {"topic": topic, "articles": extracted_data}

def main():
    """Main function to fetch research data on multiple topics concurrently."""
    topics = ["AI in HR", "Remote Work Policies", "Employee Well-being", "HR Tech Trends", "Diversity & Inclusion"]
    research_results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_topic = {executor.submit(process_topic, topic): topic for topic in topics}
        for future in concurrent.futures.as_completed(future_to_topic):
            try:
                research_results.append(future.result())
            except Exception as e:
                print(f"Error processing topic: {e}")
    
    # Close Selenium after all tasks
    driver.quit()

    # Print results as JSON
    print(json.dumps(research_results, indent=4))

if __name__ == "__main__":
    main()
