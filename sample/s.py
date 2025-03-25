import json
import boto3
from langchain_aws import ChatBedrock
from langchain.schema import SystemMessage, HumanMessage

# Initialize Amazon Bedrock client
bedrock = boto3.client(service_name="bedrock-runtime", region_name="ap-south-1")

# Initialize LangChain model wrapper
def get_bedrock_model():
    return ChatBedrock(model_id="meta.llama3-70b-instruct-v1:0")

# Function to invoke a LangChain agent
def invoke_agent(prompt, agent_name):
    try:
        model = get_bedrock_model()
        response = model([SystemMessage(content=f"{agent_name} Agent"), HumanMessage(content=prompt)])
        return response.content.strip()
    except Exception as e:
        print(f"⚠️ {agent_name} Error: {e}")
        return None

# Define blog topics
topics = [
    "Top 11 HR Trends 2025 That Will Change Future of Work",
    "59 Trending HR Buzzwords",
    "Future of Work Trends 2025: Strategic Insights for CHROs"
]

# Multi-Agent Processing
for topic in topics:
    print(f"📌 Processing: {topic}")

    # Step 1: Generate Outline
    outline_prompt = f"Generate a detailed blog outline for the topic: {topic}"
    outline = invoke_agent(outline_prompt, "Outline")
    if not outline:
        print("⚠️ Outline generation failed. Skipping topic.")
        continue

    # Step 2: Generate Content
    content_prompt = f"Write a detailed, SEO-optimized blog post based on this outline:\n{outline}"
    content = invoke_agent(content_prompt, "Content")
    if not content:
        print("⚠️ Content generation failed. Skipping topic.")
        continue

    # Step 3: Optimize for SEO
    seo_prompt = f"Optimize the following blog for SEO, improving readability and adding keywords:\n{content}"
    optimized_content = invoke_agent(seo_prompt, "SEO")
    if not optimized_content:
        print("⚠️ SEO optimization failed. Using original content.")
        optimized_content = content

    # Step 4: Save to file
    filename = topic.replace(" ", "_").lower() + ".txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(optimized_content)
    
    print(f"✅ Saved: {filename}")

print("🎉 Blog generation complete!")
