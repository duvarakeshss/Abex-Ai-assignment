import os
from huggingface_hub import InferenceClient
from langchain.tools import Tool
from dotenv import load_dotenv
from config.config import Config

# Load environment variables
load_dotenv()

class ContentGenerationAgent:
    def __init__(self):
        self.client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.1", token=Config.HF_API_KEY)
        self.max_tokens = Config.MAX_TOKENS
        self.temperature = Config.TEMPERATURE
        self.top_p = Config.TOP_P
        self.chunk_size = min(self.max_tokens, 3000 // 4)

    def generate_section(self, section_prompt):
        """Generates text for a given section using Mistral-7B."""
        response = self.client.chat_completion(
            messages=[
                {"role": "system", "content": "SEO blog"},
                {"role": "user", "content": section_prompt}
            ],
            max_tokens=self.chunk_size,
            temperature=self.temperature,
            top_p=self.top_p
        )

        return response["choices"][0]["message"]["content"]

    def generate_blog(self, outline):
        """Generates a full SEO-optimized blog from the outline."""
        sections = outline.split("\n")
        blog_content = []
        
        for section in sections:
            if section.strip():
                print(f"Generating section: {section}")
                section_content = ""
                remaining_prompt = f"Write a detailed section about: {section}"
                
                for _ in range(4):
                    chunk = self.generate_section(remaining_prompt)
                    section_content += chunk + "\n"
                    remaining_prompt = remaining_prompt[len(chunk):]
                    if len(chunk) < self.chunk_size:
                        break  
                
                blog_content.append(f"## {section}\n{section_content}")
        
        return "\n\n".join(blog_content)

    def run(self, outline):
        """Runs the content generation process."""
        print("Generating full SEO blog using Mistral-7B...")
        return self.generate_blog(outline)

# Define LangChain tool
content_tool = Tool(
    name="Content Generation Agent",
    func=ContentGenerationAgent().run,
    description="Generates a full SEO-optimized blog based on research and outline using Mistral-7B."
)
