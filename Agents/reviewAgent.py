import requests
from langchain.tools import Tool
from config import Config

class ReviewAgent:
    def __init__(self):
        """Initialize Groq API for LLaMA-3."""
        self.api_url = "https://api.groq.com/v1/chat/completions"
        self.headers = {"Authorization": f"Bearer {Config.GROQ_API_KEY}", "Content-Type": "application/json"}
        self.max_tokens = Config.MAX_TOKENS
        self.temperature = Config.TEMPERATURE
        self.top_p = Config.TOP_P

    def review_content(self, content):
        """Reviews the blog content for quality, readability, and SEO effectiveness."""
        prompt = f"""
        Review the following blog content for:
        - **Readability:** Is the content engaging and easy to understand?
        - **SEO Quality:** Are keywords naturally integrated? Is metadata optimized?
        - **Structure & Formatting:** Are headings (H1, H2, H3) properly structured?
        - **Grammar & Clarity:** Are there any spelling or grammar errors?
        - **Suggestions:** Provide specific improvement recommendations.

        Blog Content:
        {content}

        Provide a detailed review with a summary and actionable recommendations.
        """

        payload = {
            "model": "llama3-70b",
            "messages": [
                {"role": "system", "content": "You are an expert in SEO, content marketing, and writing analysis."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)

        if response.status_code == 402:
            raise Exception("Payment required: You've exceeded Groq's free-tier API limits.")

        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def run(self, content):
        """Run the content review process."""
        print("Reviewing blog content for SEO quality and readability...")
        return self.review_content(content)

# Define LangChain Tool
review_tool = Tool(
    name="Review Agent",
    func=ReviewAgent().run,
    description="Reviews blog content for SEO quality, readability, structure, and clarity using LLaMA-3 on Groq API."
)
