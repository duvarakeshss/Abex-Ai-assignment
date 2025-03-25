# # import boto3
# # import json

# # # AWS Configuration
# # AWS_REGION = "ap-south-1"  # Change this if needed
# # MODEL_ID = "meta.llama3-70b-instruct-v1:0"  # Ensure you have access to this model

# # # Initialize Bedrock Client
# # client = boto3.client("bedrock-runtime", region_name=AWS_REGION)

# # class BedrockLlamaAgent:
# #     """Handles interactions with AWS Bedrock's LLaMA 3 model."""

# #     @staticmethod
# #     def generate_text(prompt, max_tokens=2000, temperature=0.7, top_p=0.9):
# #         """Generates text using AWS Bedrock LLaMA 3 model with debugging."""
        
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

# #             # Extract generated text
# #             generated_text = response_body.get("generation", "").strip()

# #             if not generated_text:
# #                 print(f"⚠️ Empty response from Bedrock for prompt: {prompt[:100]}...")
# #                 return "⚠️ No content generated. Check AWS limits or adjust prompt."

# #             return generated_text

# #         except client.exceptions.AccessDeniedException:
# #             print("❌ AWS Access Denied! Ensure IAM role has `AmazonBedrockFullAccess` permission.")
# #             return "⚠️ AWS Access Issue!"

# #         except client.exceptions.ThrottlingException:
# #             print("❌ API Rate Limit Exceeded! Reduce API calls per minute.")
# #             return "⚠️ API Rate Limit Exceeded!"

# #         except Exception as e:
# #             print(f"❌ Unexpected Error: {e}")
# #             return "⚠️ Error in AI generation."

# # # 🚀 Test the LLaMA 3 Model
# # if __name__ == "__main__":
# #     test_prompt = "Explain the future of HR trends in 2025 in a detailed blog post."
# #     response = BedrockLlamaAgent.generate_text(test_prompt)
    
# #     # Print the generated response
# #     print("\n📄 Generated Content:\n", response)
# import boto3
# import json
# import time

# # AWS Configuration
# AWS_REGION = "ap-south-1"
# MODEL_ID = "meta.llama3-70b-instruct-v1:0"

# # Initialize Bedrock Client
# client = boto3.client("bedrock-runtime", region_name=AWS_REGION)

# class BedrockLlamaAgent:
#     """Handles interactions with AWS Bedrock's LLaMA 3 model with retry logic."""

#     @staticmethod
#     def generate_text(prompt, max_tokens=1500, temperature=0.7, top_p=0.9, retry_attempts=1):
#         """Generates text using AWS Bedrock LLaMA 3 model with error handling & retries."""
        
#         payload = {
#             "prompt": prompt,
#             "max_gen_len": max_tokens,
#             "temperature": temperature,
#             "top_p": top_p
#         }

#         attempt = 0
#         while attempt <= retry_attempts:
#             try:
#                 response = client.invoke_model(
#                     modelId=MODEL_ID,
#                     body=json.dumps(payload),
#                     contentType="application/json"
#                 )

#                 # Debug: Print raw response
#                 response_body = json.loads(response["body"].read())
#                 print("🔍 RAW RESPONSE:", response_body)

#                 # Extract generated text
#                 generated_text = response_body.get("generation", "").strip()

#                 if generated_text:
#                     return generated_text  # ✅ Successful generation
                
#                 print(f"⚠️ Empty response from Bedrock. Retrying... (Attempt {attempt+1})")
#                 attempt += 1
#                 time.sleep(2)  # 🕒 Wait before retrying

#             except client.exceptions.AccessDeniedException:
#                 return "❌ AWS Access Denied! Ensure IAM has `AmazonBedrockFullAccess`."

#             except client.exceptions.ThrottlingException:
#                 return "❌ API Rate Limit Exceeded! Reduce API calls per minute."

#             except Exception as e:
#                 return f"❌ Unexpected Error: {e}"

#         return "⚠️ No content generated after retries. Adjust prompt or check API limits."

# # 🚀 Test the LLaMA 3 Model
# if __name__ == "__main__":
#     test_prompt = "Write a blog post on HR trends in 2025."
#     response = BedrockLlamaAgent.generate_text(test_prompt)
    
#     # Print the generated response
#     print("\n📄 Generated Content:\n", response)


import boto3
import json

# Initialize Amazon Bedrock client
bedrock = boto3.client(service_name="bedrock-runtime", region_name="ap-south-1")

# Function to invoke Bedrock model (Claude or Titan)
def generate_blog_content(prompt, model="meta.llama3-70b-instruct-v1:0"):
    try:
        response = bedrock.invoke_model(
            body=json.dumps({"prompt": prompt, "max_tokens": 1000}),
            modelId=model
        )
        result = json.loads(response["body"].read())
        return result.get("generation", "").strip()
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return None

# Define blog topics
topics = [
    "Top 11 HR Trends 2025 That Will Change Future of Work",
    "59 Trending HR Buzzwords",
    "Future of Work Trends 2025: Strategic Insights for CHROs"
]

# Process each topic
for topic in topics:
    print(f"📌 Processing: {topic}")

    # Step 1: Generate Outline
    outline_prompt = f"Generate a detailed blog outline for the topic: {topic}"
    outline = generate_blog_content(outline_prompt)
    if not outline:
        print("⚠️ Outline generation failed. Skipping topic.")
        continue

    # Step 2: Generate Content
    content_prompt = f"Write a detailed, SEO-optimized blog post based on this outline:\n{outline}"
    content = generate_blog_content(content_prompt)
    if not content:
        print("⚠️ Content generation failed. Skipping topic.")
        continue

    # Step 3: Optimize for SEO
    seo_prompt = f"Optimize the following blog for SEO, improving readability and adding keywords:\n{content}"
    optimized_content = generate_blog_content(seo_prompt)
    if not optimized_content:
        print("⚠️ SEO optimization failed. Using original content.")
        optimized_content = content

    # Step 4: Save to file
    filename = topic.replace(" ", "_").lower() + ".txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(optimized_content)
    
    print(f"✅ Saved: {filename}")

print("🎉 Blog generation complete!")
