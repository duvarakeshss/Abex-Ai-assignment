# **Multi-Agent SEO Blog Generator**

This project is an **AI-powered SEO Blog Generator**  
It utilizes for research,**Mistral-7B-Instruct-v0.1** for outline creation,**LLaMA-3 via Groq API** for content generation, SEO optimization, and final review.

## **Features**
- **Automated Research**: Fetches real-time data on given topics.  
- **Structured Outline**: Generates a well-organized blog structure.  
- **Content Generation**: Writes detailed, high-quality SEO content.  
- **SEO Optimization**: Enhances blog for better ranking & readability.  
- **Final Review**: Ensures content quality, keyword density & structure.

---

## **Project Approach**
1. **ResearchAgent** → Search and gathers relevant information using serapi from google search.
2. **OutlineAgent** → Creates a structured blog outline using **Mistral-7B-Instruct-v0.1**.
3. **ContentGenerationAgent** → Writes the blog using **LLaMA-3 on Groq**.
4. **SEOOptimizationAgent** → Improves SEO ranking & keyword usage.
5. **ReviewAgent** → Checks grammar, readability, and SEO effectiveness.

---

## **File Structure**
 
 ┣ Agents
 ┃ ┣ researchAgent.py            # Fetches topic-related research
 ┃ ┣ outlineAgent.py             # Generates blog outline
 ┃ ┣ contentGenerationAgent.py   # Generates full blog content
 ┃ ┣ seoOptimizerAgent.py        # Optimizes content for SEO
 ┃ ┣ reviewAgent.py              # Final content review
 ┃
 ┣ config.py                     # Stores API keys & model settings
 ┣ .env                          # API keys (Groq, Hugging Face, etc.)
 ┃
 ┣  main.py                      # Main execution script
 ┣ requirements.txt              # Python dependencies
 ┣ README.md                     # Project documentation
 ┗ generated_blog.txt            # Output file (Final optimized blog)



