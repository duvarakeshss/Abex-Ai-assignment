# # # # import boto3
# # # # import json

# # # # # AWS Bedrock Runtime client (Ensure region is correct)
# # # # client = boto3.client("bedrock-runtime", region_name="ap-south-1")

# # # # # Correct Model ID from your AWS response
# # # # model_id = "meta.llama3-70b-instruct-v1:0"

# # # # # Define prompt for Llama 3
# # # # prompt_text = "What are the benefits of using AWS Bedrock for LLMs?"

# # # # # Construct payload
# # # # payload = {
# # # #     "prompt": prompt_text,
# # # #     "max_gen_len": 512,
# # # #     "temperature": 0.7,
# # # #     "top_p": 0.9
# # # # }

# # # # # Invoke the model
# # # # try:
# # # #     response = client.invoke_model(
# # # #         modelId=model_id,  # Corrected model ID
# # # #         body=json.dumps(payload),
# # # #         contentType="application/json"
# # # #     )

# # # #     # Read and parse response
# # # #     response_body = json.loads(response["body"].read())
# # # #     print("Llama 3 Response:\n", response_body)
# # # #     print("Llama 3 Response:\n", response_body["generation"])


# # # # except Exception as e:
# # # #     print("Error:", str(e))


# # import boto3
# # import json

# # # AWS Bedrock setup
# # REGION = "ap-south-1"
# # MODEL_ID = "meta.llama3-70b-instruct-v1:0"  # Ensure this matches your Bedrock model

# # # Initialize Bedrock client
# # client = boto3.client("bedrock-runtime", region_name=REGION)

# # # Test prompt
# # payload = {
# #     "prompt": "List 5 future HR trends.",
# #     "max_gen_len": 512,
# #     "temperature": 0.7,
# #     "top_p": 0.9
# # }

# # # try:
# # #     response = client.invoke_model(
# # #         modelId=MODEL_ID,
# # #         body=json.dumps(payload),
# # #         contentType="application/json"
# # #     )
    
# # #     # Print raw response
# # #     response_body = json.loads(response["body"].read())
# # #     print("🔍 Bedrock Response:", response_body)

# # # except Exception as e:
# # #     print("❌ Error calling Bedrock:", str(e))

# # class BedrockLlamaAgent:
# #     """Handles interactions with AWS Bedrock's LLaMA 3 model."""

# #     @staticmethod
# #     def generate_text(prompt, max_tokens=512, temperature=0.7, top_p=0.9):
# #         payload = {
# #             "prompt": prompt,
# #             "max_gen_len": max_tokens,
# #             "temperature": temperature,
# #             "top_p": top_p
# #         }

# #         try:
# #             response = client.invoke_model(
# #                 modelId=MODEL_ID,
# #                 body=json.dumps(payload),
# #                 contentType="application/json"
# #             )

# #             # Debug: Print raw response
# #             response_body = json.loads(response["body"].read())
# #             print("🔍 RAW RESPONSE:", response_body)

# #             # Extracting generated text
# #             generated_text = response_body.get("generation", "").strip()
            
# #             if not generated_text:
# #                 print("⚠️ Empty response from Bedrock. Adjust prompt or check API limits.")
# #                 return "⚠️ No content generated."

# #             return generated_text

# #         except Exception as e:
# #             print(f"❌ Error calling Bedrock LLaMA: {e}")
# #             return "⚠️ Error in AI generation."


# import boto3
# import json

# # Initialize AWS Bedrock client
# client = boto3.client("bedrock-runtime", region_name="ap-south-1")

# # Correct Bedrock LLaMA Model ID
# MODEL_ID = "meta.llama3-70b-instruct-v1:0"

# class BedrockLlamaAgent:
#     """Handles interactions with AWS Bedrock's LLaMA 3 model."""

#     @staticmethod
#     def generate_text(prompt, max_tokens=512, temperature=0.7, top_p=0.9):
#         payload = {
#             "prompt": prompt,
#             "max_gen_len": max_tokens,
#             "temperature": temperature,
#             "top_p": top_p
#         }

#         try:
#             response = client.invoke_model(
#                 modelId=MODEL_ID,
#                 body=json.dumps(payload),
#                 contentType="application/json"
#             )

#             # Debug: Print raw response
#             response_body = json.loads(response["body"].read())
#             print("🔍 RAW RESPONSE:", response_body)

#             # Extracting generated text
#             generated_text = response_body.get("generation", "").strip()
            
#             if not generated_text:
#                 print("⚠️ Empty response from Bedrock. Adjust prompt or check API limits.")
#                 return "⚠️ No content generated."

#             return generated_text

#         except Exception as e:
#             print(f"❌ Error calling Bedrock LLaMA: {e}")
#             return "⚠️ Error in AI generation."

# # 🔥 Run standalone test
# if __name__ == "__main__":
#     test_prompt = "What are the benefits of using AWS Bedrock for LLMs?"
#     response = BedrockLlamaAgent.generate_text(test_prompt)
    
#     print("\n📝 Llama 3 Output:\n", response)

#     # Save response to file
#     if response.strip():
#         with open("test_output.txt", "w", encoding="utf-8") as f:
#             f.write(response)
#         print("\n✅ Output saved to test_output.txt")

import os
import json
import boto3
import requests
from bs4 import BeautifulSoup

# AWS Bedrock Configuration
AWS_REGION = "ap-south-1"  # Update this based on your AWS account
MODEL_ID = "meta.llama3-70b-instruct-v1:0"

# Initialize AWS Bedrock Client
client = boto3.client("bedrock-runtime", region_name=AWS_REGION)

# User-Agent to avoid bot detection
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

class BedrockLlamaAgent:
    """Handles interactions with AWS Bedrock's LLaMA 3 model."""

    @staticmethod
    def generate_text(prompt, max_tokens=2000, temperature=0.7, top_p=0.9):
        """Generates text using AWS Bedrock LLaMA 3 model with enhanced debugging."""
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

            # Read and parse response
            response_body = json.loads(response["body"].read())
            generated_text = response_body.get("generation", "").strip()

            if not generated_text:
                print(f"⚠️ Empty response from Bedrock for prompt: {prompt[:100]}...")
                return "⚠️ No content generated. Check AWS limits or adjust prompt."

            return generated_text

        except client.exceptions.AccessDeniedException:
            print("❌ AWS Access Denied! Ensure IAM role has `AmazonBedrockFullAccess` permission.")
            return "⚠️ AWS Access Issue!"

        except client.exceptions.ThrottlingException:
            print("❌ API Rate Limit Exceeded! Reduce API calls per minute.")
            return "⚠️ API Rate Limit Exceeded!"

        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            return "⚠️ Error in AI generation."

class ResearchAgent:
    """Finds trending HR topics and relevant news articles."""

    def fetch_trending_topics(self):
        """Scrapes Google News for trending HR topics."""
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
        return BedrockLlamaAgent.generate_text(prompt, max_tokens=700)

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

    def save_to_file(self, filename, content):
        """Saves the generated blog content to a .txt file."""
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"📄 Blog saved as {filename}")

    def run(self):
        print("🔍 Researching trending topics...")
        topics = self.research_agent.fetch_trending_topics()

        for topic in topics:
            print(f"\n📌 Processing: {topic}")

            print("📝 Generating blog outline...")
            outline = self.planning_agent.generate_outline(topic)
            if not outline or "⚠️" in outline:
                print("⚠️ Skipping topic due to outline generation failure.")
                continue

            print("✍️ Generating content...")
            content = self.generation_agent.generate_content(outline)
            if not content or "⚠️" in content:
                print("⚠️ Skipping topic due to content generation failure.")
                continue

            print("🔍 Optimizing for SEO...")
            optimized_content = self.seo_agent.optimize_content(content)

            print("🧐 Reviewing content...")
            final_content = self.review_agent.review_content(optimized_content)

            if final_content and "⚠️" not in final_content:
                filename = f"{topic.replace(' ', '_')}.txt"
                self.save_to_file(filename, final_content)
            else:
                print("⚠️ Empty content. Skipping file save.")

if __name__ == "__main__":
    system = MultiAgentBlogSystem()
    system.run()
