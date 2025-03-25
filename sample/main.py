import os
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain_community.llms import HuggingFacePipeline
from huggingface_hub import login

HF_TOKEN = "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"

# Model details
model_name = "meta-llama/Meta-Llama-3-8B-Instruct"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=HF_TOKEN)
model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=HF_TOKEN)

# Initialize LLM with LangChain
llm = HuggingFacePipeline(model=model, tokenizer=tokenizer)

# Example prompt
prompt = "Explain quantum physics in simple terms."
response = llm(prompt)
print(response)
