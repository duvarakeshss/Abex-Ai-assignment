import requests
import time

# SerpAPI Configuration
SERP_API_KEY = "32b4b327fef8a812de7734f5a94219ff236a76ebe053b51f6c7ff0108aa6573e"
SEARCH_QUERY = "HR trends 2024"
SERP_API_URL = "https://serpapi.com/search"

# AI-Agent API Configuration
AI_API_URL = "https://i1yx0nrndh.execute-api.ap-south-1.amazonaws.com/default/ai-agent"

# SEO Blog Writing Template
SEO_BLOG_TEMPLATE = """
SEO Blog Writing Template
1. Title (H1)
2. Meta Description
3. Introduction (H2)
4. Main Body (H2 & H3)
    - Key HR Trends (AI, Compensation, DEI, Hybrid Work)
5. Conclusion (H2)
6. SEO Checklist
"""

# Fetch multiple pages of search results from SerpAPI
def fetch_serp_results(query, pages=3):
    all_snippets = []
    for page in range(1, pages + 1):
        params = {
            "q": query,
            "engine": "google",
            "api_key": SERP_API_KEY,
            "start": (page - 1) * 10  # Pagination
        }
        try:
            response = requests.get(SERP_API_URL, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            if "organic_results" in data:
                for result in data["organic_results"]:
                    if "title" in result and "snippet" in result:
                        all_snippets.append(f"{result['title']}: {result['snippet']}")

            time.sleep(2)  # Prevent rate limits
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")

    return " ".join(all_snippets)[:3000]  # Limit snippet size

# Generate SEO blog chunks to prevent crashes
def generate_seo_chunks(content, chunk_size=400):
    blog_chunks = []
    content_parts = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]

    for idx, part in enumerate(content_parts):
        print(f"Generating chunk {idx+1}/{len(content_parts)}...")
        payload = {
            "inputs": f"Write a detailed blog section for don't add your thinking just wirte the the blog alone:\n{part}\n\n{SEO_BLOG_TEMPLATE}",
            "parameters": {"max_tokens": chunk_size, "temperature": 0.7, "top_p": 0.9}
        }
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(AI_API_URL, json=payload, headers=headers, timeout=90)
            response.raise_for_status()
            blog_chunks.append(response.json().get("response", ""))
        except requests.exceptions.RequestException as e:
            print(f"Error in chunk {idx+1}: {e}")

    return "\n".join(blog_chunks)

# Execute the pipeline
if __name__ == "__main__":
    print("Fetching search data...")
    search_content = fetch_serp_results(SEARCH_QUERY)

    if search_content:
        print("Generating SEO blog in chunks...")
        complete_blog = generate_seo_chunks(search_content, chunk_size=400)

        if complete_blog:
            print("=== GENERATED SEO BLOG ===")
            print(complete_blog)
