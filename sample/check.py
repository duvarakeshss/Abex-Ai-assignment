import requests
import time

# === CONFIGURATION ===
SERP_API_KEY = "32b4b327fef8a812de7734f5a94219ff236a76ebe053b51f6c7ff0108aa6573e"  # Replace with your actual SerpAPI key
AI_API_URL = "https://i1yx0nrndh.execute-api.ap-south-1.amazonaws.com/default/ai-agent"
SEARCH_QUERY = "trending HR-related topic"
SERP_API_URL = "https://serpapi.com/search"

# === FETCH SEARCH RESULTS FROM SERPAPI ===
def fetch_serp_results(query):
    params = {
        "q": query,
        "engine": "google",
        "api_key": SERP_API_KEY
    }
    response = requests.get(SERP_API_URL, params=params)
    if response.status_code == 200:
        return response.json()  # Returns SERP JSON data
    else:
        print("Error fetching SERP results:", response.text)
        return None

# === EXTRACT CONTENT FROM SERP RESULTS ===
def extract_content_from_serp(data):
    snippets = []
    if "organic_results" in data:
        for result in data["organic_results"]:
            if "snippet" in result:
                snippets.append(result["snippet"])
    return " ".join(snippets)  # Concatenate all snippets

# === GENERATE LONG SEO BLOG IN CHUNKS ===
def generate_large_content(prompt, chunk_size=800, max_chunks=5, delay=2):
    full_text = ""
    for i in range(max_chunks):
        print(f"Generating chunk {i+1}...")  # Debugging info

        payload = {
            "inputs": prompt,
            "parameters": {"max_tokens": chunk_size}
        }
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(AI_API_URL, json=payload, headers=headers, timeout=120)
            if response.status_code == 200:
                output = response.json().get("response", "")
                full_text += output + "\n"
                prompt += output  # Continue from last output
                time.sleep(delay)  # Prevent API rate limiting
            else:
                print("Error:", response.text)
                break

        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
            break

    return full_text

# === SEO BLOG TEMPLATE ===
SEO_BLOG_TEMPLATE = """
SEO Blog Writing Template
1. Title (H1)
Include the primary keyword. Keep it under 60 characters.
Example: “10 Best Strategies for SEO in 2024”

2. Meta Description
150–160 characters long. Include the primary keyword naturally.

3. Introduction (H2)
Hook the reader with an engaging question or statistic.
Briefly introduce the topic and its importance.

4. Main Body (Use H2 and H3 Headings)
4.1. First Subtopic (H2) - Explain the first key point.
4.2. Second Subtopic (H2) - Keep paragraphs short.
4.3. Third Subtopic (H2) - Add real-life examples, case studies.

5. Conclusion (H2)
Summarize key takeaways and encourage engagement.

6. SEO Checklist
✅ Keywords included naturally.
✅ Meta description, title, and headings optimized.
✅ Internal and external links added.
"""

# === RUN THE PIPELINE ===
serp_data = fetch_serp_results(SEARCH_QUERY)
if serp_data:
    content = extract_content_from_serp(serp_data)
    print("Extracted Content:", content[:500])  # Debug: Show first 500 chars

    prompt = f"Generate a 3000-word SEO blog following this outline:\n{content}\n\n{SEO_BLOG_TEMPLATE}"
    long_article = generate_large_content(prompt)
    
    print("\n\n=== GENERATED SEO BLOG ===\n")
    print(long_article)
