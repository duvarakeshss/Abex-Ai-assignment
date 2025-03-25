import os
import json
import boto3
import requests
from bs4 import BeautifulSoup

# AWS Bedrock Configuration
REGION = "ap-south-1"  # Update to your AWS region
MODEL_ID = "meta.llama3-70b-instruct-v1:0"  # LLaMA 3 model ID

# Initialize AWS Bedrock client
client = boto3.client("bedrock-runtime", region_name=REGION)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


class BedrockLlamaAgent:
    """Handles interactions with AWS Bedrock's LLaMA 3 model."""

    @staticmethod
    def generate_text(prompt, max_tokens=512, temperature=0.7, top_p=0.9):
        payload = {
            "prompt": prompt,
            "max_gen_len": max_tokens,
            "temperature": temperature,
            "top_p": top_p
        }

        try:
            response = client.invoke_model(
                modelId=MODEL_ID,
                body=json.dumps(payload),
                contentType="application/json"
            )

            response_body = json.loads(response["body"].read())
            return response_body.get("generation", "").strip()

        except Exception as e:
            print(f"❌ Error calling Bedrock LLaMA: {e}")
            return ""


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
        return BedrockLlamaAgent.generate_text(prompt, max_tokens=500)


class ContentGenerationAgent:
    """Writes a well-structured blog post based on the outline."""

    def generate_content(self, outline):
        if not outline:
            print("⚠️ Skipping content generation due to missing outline.")
            return ""

        prompt = f"Write a detailed blog post following this outline:\n\n{outline}"
        return BedrockLlamaAgent.generate_text(prompt, max_tokens=1500)


class SEOOptimizationAgent:
    """Ensures the content follows SEO best practices."""

    def optimize_content(self, content):
        if not content:
            print("⚠️ Skipping SEO optimization due to missing content.")
            return ""

        prompt = f"Optimize the following blog content for SEO, improving readability and adding relevant keywords:\n\n{content}"
        return BedrockLlamaAgent.generate_text(prompt, max_tokens=1000)


class ReviewAgent:
    """Proofreads and improves content quality."""

    def review_content(self, content):
        if not content:
            print("⚠️ Skipping review due to missing content.")
            return ""

        prompt = f"Proofread and enhance the quality of this blog post:\n\n{content}"
        return BedrockLlamaAgent.generate_text(prompt, max_tokens=1000)


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

            if final_content:
                print("\n✅ Final Blog Post:\n", final_content)
                self.save_as_txt(topic, final_content)
            else:
                print("⚠️ Empty content. Skipping file save.")

    @staticmethod
    def save_as_txt(title, content):
        """Saves the final blog post as a .txt file."""
        filename = f"{title.replace(' ', '_')}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"📄 Blog saved as: {filename}")


if __name__ == "__main__":
    system = MultiAgentBlogSystem()
    system.run()
