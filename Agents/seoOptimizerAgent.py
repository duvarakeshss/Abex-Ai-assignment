import requests
from langchain.tools import Tool
from config.config import Config

class SEOOptimizationAgent:
    def __init__(self):
        """Initialize Groq API for LLaMA-3."""
        
        self.api_url = "https://api.groq.com/v1/chat/completions"
        self.headers = {"Authorization": f"Bearer {Config.GROQ_API_KEY}", "Content-Type": "application/json"}
        self.max_tokens = Config.MAX_TOKENS
        self.temperature = Config.TEMPERATURE
        self.top_p = Config.TOP_P

    def optimize_content(self, content):
        """Enhances blog content for SEO using LLaMA-3 via Groq API."""
        prompt = f"""
        Optimize the following blog for SEO:
        - Improve readability and structure.
        - Enhance keyword optimization (without keyword stuffing).
        - Ensure engaging meta descriptions.
        - Format headings correctly (H1, H2, H3).
        - Add missing SEO best practices.

        Blog Content:
        {content}

        Optimized SEO Content:
        """

        payload = {
            "model": "llama3-70b",
            "messages": [
                {"role": "system", "content": "SEO optimization."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)

        if response.status_code == 402:
            raise Exception("exceeded Groq's free-tier API limits.")

        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def run(self, content):
        """Run the SEO optimization process."""
        print("Optimizing content for SEO using LLaMA-3 on Groq API...")
        return self.optimize_content(content)

# Define LangChain Tool
seo_tool = Tool(
    name="SEO Optimization Agent",
    func=SEOOptimizationAgent().run,
    description="Enhances blog content for SEO using LLaMA-3 on Groq API."
)
