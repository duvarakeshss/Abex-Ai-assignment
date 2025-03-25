import os
from Agents.researchAgent import ResearchAgent
from Agents.outlineAgent import OutlineAgent
from Agents.contentGenerationAgent import ContentGenerationAgent
from Agents.seoOptimizerAgent import SEOOptimizationAgent
from Agents.reviewAgent import ReviewAgent
from config import Config

def main():
    print("Fetching research data")
    research_agent = ResearchAgent()
    search_data = research_agent.run(Config.SEARCH_QUERY)
    
    if not search_data:
        print("Failed to retrieve research data. Exiting.")
        return
    
    print("Generating SEO blog outline")
    outline_agent = OutlineAgent()
    blog_outline = outline_agent.run(search_data)
    
    if not blog_outline:
        print("Failed to generate an outline. Exiting.")
        return
    
    print("Generating full blog content...")
    content_agent = ContentGenerationAgent()
    blog_content = content_agent.run(blog_outline)
    
    if not blog_content:
        print("Failed to generate blog content. Exiting.")
        return

    print("Optimizing blog for SEO...")
    seo_agent = SEOOptimizationAgent()
    optimized_content = seo_agent.run(blog_content)

    if not optimized_content:
        print("Failed to optimize blog content for SEO. Exiting.")
        return

    print("Running final review for SEO & readability...")
    review_agent = ReviewAgent()
    review_feedback = review_agent.run(optimized_content)

    if not review_feedback:
        print("Failed to review blog content. Exiting.")
        return

    output_file = "generated_blog.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(optimized_content)

if __name__ == "__main__":
    main()
