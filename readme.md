# **Multi-Agent SEO Blog Generator**

This project is an **AI-powered SEO Blog Generator**
It utilizes serp for research,**Mistral-7B-Instruct-v0.1** for outline creation,**LLaMA-3 via Groq** for content generation, SEO optimization, and final review.

## **Features**

- **Automated Research**: Fetches real-time data on given topics.
- **Structured Outline**: Generates a well-organized blog structure.
- **Content Generation**: Writes detailed, high-quality SEO content.
- **SEO Optimization**: Enhances blog for better ranking & readability.
- **Final Review**: Ensures content quality, keyword density & structure.

---

## **Key Approach**

1. **ResearchAgent** → Search and gathers relevant information using serapi from google search.
2. **OutlineAgent** → Creates a structured blog outline using **Mistral-7B-Instruct-v0.1**.
3. **ContentGenerationAgent** → Writes the blog using **LLaMA-3 on Groq**.
4. **SEOOptimizationAgent** → Improves SEO ranking & keyword usage.
5. **ReviewAgent** → Checks grammar, readability, and SEO effectiveness.

---

## **File Structure**
```
Abex-Ai-assignment/
├── Agents/
│ ├── researchAgent.py
│ ├── outlineAgent.py
│ ├── contentGenerationAgent.py
│ ├── seoOptimizerAgent.py
│ ├── reviewAgent.py
├── Config/
| |── config.py
| ├── .env
├── main.py
├── requirements.txt
├── README.md
├── output/
| ├── generated_blog.txt
```
---

## How to Set Up & Run

### Clone the Repository

```sh
git clone https://github.com/duvarakeshss/Abex-Ai-assignment
cd Abex-Ai-assignment
```

### Create a Virtual Environment

```sh
python -m venv venv
```

### Activate Virtual Environment

Windows

```sh
venv\Scripts\Activate
```

Mac/Linux

```sh
source venv/bin/activate
```

### Install Dependencies

```sh
pip install -r requirements.txt
```

### Run the Project

```sh
python main.py
```
# Report

## **Problem Statement**  
The goal was to create an automated system that generates high-quality, SEO-optimized blog posts using multiple AI agents. The system needed to research topics, generate structured content, optimize for SEO, and ensure content quality through review.

---
## **Initial Approach**

## **Approach**  

### **1. Initial Approach - AWS SageMaker Deployment**  
- Initially, I deployed a **LLaMA 70B model** on **AWS SageMaker** for text generation.  
- Fine-tuned the model in AWS to improve content generation quality.  
- Successfully integrated the model into the system to generate research-based blogs.  

#### **Challenges Faced**  
- **Billing Issues:** Due to high usage, AWS SageMaker costs increased.  
- **Free Tier Expired:** Once the free credits were exhausted, further model fine-tuning and inference became costly.  
- **Solution:** Switched to a more cost-effective alternative—Hugging Face Inference API.  

---

### **2. Transition to Hugging Face**  
- Used **Hugging Face Inference API** to replace SageMaker for model inference.  
- Deployed **Mistral-7B** for text generation instead of LLaMA.  
- Integrated Hugging Face’s model endpoints into the existing pipeline.  

#### **Challenges Faced**  
- **API Limitations:** Faced request limits and required a paid plan for continuous access.  
- **Solution:** Adjusted API calls to optimize token usage and ensure cost-effective querying.  

---

### **3. Adopting Groq LLaMA Model**  
- To further optimize costs and performance, I switched to **Groq’s LLaMA model**.  
- Integrated Groq’s API for inference, ensuring scalability and affordability.  
- Maintained the multi-agent architecture while improving performance.  

---

## **Multi-Agent System Breakdown**  

The solution was designed using **modular AI agents**, each responsible for a specific task:  

1. **Research Agent** – Scrapes the web to gather relevant topic information.  
2. **Outline Agent** – Structures the blog into a detailed, well-organized outline.  
3. **Content Generation Agent** – Writes the full blog based on the outline.  
4. **SEO Optimization Agent** – Enhances blog content for search engine ranking.  
5. **Review Agent** – Checks content quality, readability, and coherence.  

Each agent works independently and sequentially to ensure automation and efficiency.  

---

## **Challenges and Solutions**  

| Challenge | Solution |
|-----------|----------|
| High AWS SageMaker costs | Switched to Hugging Face API |
| Hugging Face API limits | Optimized API usage & switched to Groq LLaMA |
| Ensuring SEO optimization | Built a dedicated SEO Optimization Agent |
| Maintaining high-quality content | Implemented a Review Agent for quality checks |

---

## **Conclusion**  
Through an iterative process, I transitioned from AWS SageMaker to Hugging Face and finally to **Groq’s LLaMA model**, optimizing for both cost and efficiency. The multi-agent architecture ensures an automated, scalable, and high-quality SEO blog generation system. 


## **Final Approach**  

### **1. Understanding the Requirements**  
- The system needed to work autonomously, with multiple specialized agents handling different stages of blog generation.  
- It had to integrate a language model for text generation.  
- The content had to be structured, optimized for SEO, and reviewed before finalization.  

### **2. Breaking Down the Problem into Subtasks**  
To achieve modularity and efficiency, the problem was divided into the following agents:  

1. **Research Agent** – Gathers topic-related information from the web.  
2. **Outline Agent** – Creates a structured outline for the blog.  
3. **Content Generation Agent** – Writes the full blog content.  
4. **SEO Optimization Agent** – Enhances the blog for search engines.  
5. **Review Agent** – Ensures quality, coherence, and correctness.  

---

## **Implementation Steps**  

### **1. Setting Up the Environment**  
- Used Python as the primary language.  
- Managed dependencies with a virtual environment.  
- Integrated Groq’s LLaMA model for text generation.  

### **2. Developing Each Agent**  
- **Research Agent:** Used web scraping/APIs to fetch relevant data.  
- **Outline Agent:** Used AI prompts to generate structured blog outlines.  
- **Content Agent:** Generated detailed sections based on the outline.  
- **SEO Agent:** Optimized titles, meta descriptions, and keyword usage.  
- **Review Agent:** Ensured readability, grammar correctness, and factual consistency.  

### **3. Integrating the Agents**  
- Connected all agents in a pipeline where each step’s output became the next step’s input.  
- Used LangChain for structuring interactions between agents.  
- Handled API calls efficiently to ensure smooth processing.  

### **4. Testing and Debugging**  
- Identified and fixed API errors, model response inconsistencies, and formatting issues.  
- Adjusted prompts and parameters for better content quality.  
- Ensured all agents worked together seamlessly.  

---

## **Challenges and Solutions**  

### **1. API Limitations**  
- Encountered API rate limits and costs with Hugging Face’s inference endpoints.  
- **Solution:** Switched to Groq’s LLaMA model for cost-effective inference.  

### **2. Model Response Formatting**  
- Some AI responses were unstructured or redundant.  
- **Solution:** Improved prompt engineering and response parsing.  

### **3. SEO Optimization**  
- Ensuring keyword density and readability without keyword stuffing was challenging.  
- **Solution:** Used predefined SEO rules and automated analysis tools.  

---

## **Conclusion**  
By breaking the problem into modular agents, leveraging AI effectively, and iterating through testing, the project successfully automated SEO blog generation. The system ensures high-quality content with minimal human intervention, making it a scalable and efficient solution.


