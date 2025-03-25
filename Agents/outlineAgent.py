import requests
from langchain.tools import Tool
from config import Config

class OutlineAgent:
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

    def generate_outline(self, content):
        """Generate SEO blog outline using DeepSeek API in chunks"""
        payload_template = {
            "inputs": "",
            "parameters": {
                "max_tokens": Config.MAX_TOKENS // 4,  # Split into 4 chunks
                "temperature": Config.TEMPERATURE,
                "top_p": Config.TOP_P,
            },
        }

        sections = [
            "Title and Meta Description",
            "Introduction and Key HR Trends",
            "Conclusion and SEO Checklist",
        ]

        blog_output = []

        for section in sections:
            print(f"🔹 Generating: {section}...")

            payload = payload_template.copy()
            payload["inputs"] = f"Generate the {section} based on:\n{content}\n\n{self.SEO_BLOG_TEMPLATE}"

            response = requests.post(Config.DEEPSEEK_API_URL, json=payload, timeout=120)
            response.raise_for_status()

            chunk = response.json().get("response", "Error generating content")
            blog_output.append(chunk)

        return "\n\n".join(blog_output)

    def run(self, content):
        print("Generating SEO blog outline in chunks")
        return self.generate_outline(content)

outline_tool = Tool(
    name="Outline Agent",
    func=OutlineAgent().run,
    description="Generates an SEO blog outline "
)
