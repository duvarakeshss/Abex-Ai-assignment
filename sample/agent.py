import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# Load API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key! Set OPENAI_API_KEY in environment variables.")

client = OpenAI(api_key=OPENAI_API_KEY)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

class ResearchAgent:
    """Finds trending HR topics and relevant news articles."""

    def fetch_trending_topics(self):
        url = "https://www.google.com/search?q=trending+HR+topics&tbm=nws"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        topics = []
        for item in soup.select(".SoaBEf"):
            title_tag = item.select_one(".nDgy9d")
            if title_tag:
                topics.append(title_tag.text)

        return topics[:5]  # Return top 5 trending topics


class ContentPlanningAgent:
    """Creates a structured blog outline based on the topic."""

    def generate_outline(self, topic):
        prompt = f"Generate a detailed blog outline for the topic: {topic}"
        try:
            response = client.completions.create(
                model="gpt-4o",  # Corrected model name
                prompt=prompt,
                max_tokens=500  # Limit response length
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Error generating outline: {e}")
            return ""


class ContentGenerationAgent:
    """Writes a well-structured blog post based on the outline."""

    def generate_content(self, outline):
        if not outline:
            print("Skipping content generation due to missing outline.")
            return ""

        prompt = f"Write a detailed blog post following this outline:\n\n{outline}"
        try:
            response = client.completions.create(
                model="gpt-4o",
                prompt=prompt,
                max_tokens=1500
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Error generating content: {e}")
            return ""


class SEOOptimizationAgent:
    """Ensures the content follows SEO best practices."""

    def optimize_content(self, content):
        if not content:
            print("Skipping SEO optimization due to missing content.")
            return ""

        prompt = f"Optimize the following blog content for SEO, improving readability and adding relevant keywords:\n\n{content}"
        try:
            response = client.completions.create(
                model="gpt-4o",
                prompt=prompt,
                max_tokens=1000
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Error optimizing content: {e}")
            return ""


class ReviewAgent:
    """Proofreads and improves content quality."""

    def review_content(self, content):
        if not content:
            print("Skipping review due to missing content.")
            return ""

        prompt = f"Proofread and enhance the quality of this blog post:\n\n{content}"
        try:
            response = client.completions.create(
                model="gpt-4o",
                prompt=prompt,
                max_tokens=1000
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Error reviewing content: {e}")
            return ""


class MultiAgentBlogSystem:
    """Orchestrates the multi-agent workflow."""

    def __init__(self):
        self.research_agent = ResearchAgent()
        self.planning_agent = ContentPlanningAgent()
        self.generation_agent = ContentGenerationAgent()
        self.seo_agent = SEOOptimizationAgent()
        self.review_agent = ReviewAgent()

    def run(self):
        print("🔍 Researching trending topics...")
        topics = self.research_agent.fetch_trending_topics()

        for topic in topics:
            print(f"\n📌 Processing: {topic}")

            print("📝 Generating blog outline...")
            outline = self.planning_agent.generate_outline(topic)
            if not outline:
                print("⚠️ Skipping topic due to outline generation failure.")
                continue

            print("✍️ Generating content...")
            content = self.generation_agent.generate_content(outline)
            if not content:
                print("⚠️ Skipping topic due to content generation failure.")
                continue

            print("🔍 Optimizing for SEO...")
            optimized_content = self.seo_agent.optimize_content(content)

            print("🧐 Reviewing content...")
            final_content = self.review_agent.review_content(optimized_content)

            print("\n✅ Final Blog Post:\n", final_content)


if __name__ == "__main__":
    system = MultiAgentBlogSystem()
    system.run()
