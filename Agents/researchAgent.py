import requests
from langchain.tools import Tool
from config import Config

class ResearchAgent:
    def fetch_serp_results(self, query):
        """Fetch search data from SerpAPI"""
        params = {"q": query, "engine": "google", "api_key": Config.SERP_API_KEY}
        response = requests.get(Config.SERP_API_URL, params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def extract_content(self, data):
        """Extract relevant content from search results"""
        return " ".join(
            [f"{res['title']}: {res['snippet']}" for res in data.get("organic_results", [])]
        )[:2000]  # Limit snippet length to prevent overflow

    def run(self, query):
        print(f"Researching: {query}")
        serp_data = self.fetch_serp_results(query)
        return self.extract_content(serp_data)

research_tool = Tool(
    name="Research Agent",
    func=ResearchAgent().run,
    description="Fetches relevant content for SEO blog from search results."
)
