import requests
from langchain.tools import Tool
from config import Config

class ContentGenerationAgent:
    def __init__(self):
        self.max_tokens = Config.MAX_TOKENS
        self.temperature = Config.TEMPERATURE
        self.top_p = Config.TOP_P
        self.api_url = Config.DEEPSEEK_API_URL

    def generate_section(self, section_prompt):
        """Generate a section of the blog using DeepSeek AI."""
        payload = {
            "inputs": section_prompt,
            "parameters": {
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
            },
        }
        response = requests.post(self.api_url, json=payload, timeout=120)
        response.raise_for_status()
        return response.json().get("response", "")

    def generate_blog(self, outline):
        """Generate full blog content based on the outline."""
        sections = outline.split("\n")
        blog_content = ""
        
        for section in sections:
            if section.strip():  # Ensure it's not an empty line
                print(f"📝 Generating section: {section}")
                blog_content += f"\n## {section}\n"
                blog_content += self.generate_section(f"Write a detailed section about: {section}")
                
        return blog_content

    def run(self, outline):
        print("Generating full SEO blog...")
        return self.generate_blog(outline)

content_tool = Tool(
    name="Content Generation Agent",
    func=ContentGenerationAgent().run,
    description="Generates a full SEO-optimized blog based on research and outline using DeepSeek."
)

