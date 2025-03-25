import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from config import Config
from langchain.tools import Tool

# Load environment variables
load_dotenv()

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

    def __init__(self):
        """Initialize the Hugging Face Inference Client."""
        self.client = InferenceClient(api_key=Config.HF_API_KEY)

    def generate_outline(self, content):
        """Generate SEO blog outline using Hugging Face model."""
        sections = [
            "Title and Meta Description",
            "Introduction and Key HR Trends",
            "Conclusion and SEO Checklist",
        ]

        blog_output = []

        for section in sections:
            print(f"Generating: {section}...")

            prompt = f"Generate the proper outline {section} based on:\n{content}\n\n{self.SEO_BLOG_TEMPLATE}"

            response = self.client.chat_completion(
                model="mistralai/Mistral-7B-Instruct-v0.1",
                messages=[
                    {"role": "system", "content": "create the detailed blog of 3000 words"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=Config.MAX_TOKENS // 4,
                temperature=Config.TEMPERATURE,
                top_p=Config.TOP_P
            )

            generated_text = response.choices[0].message["content"]
            print(generated_text)  # Print generated content
            blog_output.append(generated_text)

        return "\n\n".join(blog_output)

    def run(self, content):
        """Run the outline generation process."""
        print("Generating SEO blog outline...")
        return self.generate_outline(content)

# Define the LangChain tool
outline_tool = Tool(
    name="Outline Agent",
    func=OutlineAgent().run,
    description="Generates an SEO blog outline"
)
