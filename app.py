import os
import streamlit as st
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

# Load API keys and configuration from .env
load_dotenv()

# Set Streamlit page configuration
st.set_page_config(page_title="Agentic Newsletter Generator", page_icon="🧠", layout="wide")

# App Header
st.title("🧠 Agentic Newsletter Generator")
st.markdown("Leverage multi-agent AI powered by CrewAI and Cohere's C-R7B for generating insightful articles.")

# Sidebar: Input controls
with st.sidebar:
    st.header("🛠️ Generator Settings")

    user_topic = st.text_area(
        label="Topic of Interest",
        placeholder="e.g. The impact of AI in modern education",
        height=100
    )

    creativity = st.slider("Creativity (Temperature)", min_value=0.0, max_value=1.0, value=0.7)

    generate_clicked = st.button("🚀 Generate Newsletter", use_container_width=True)

    with st.expander("ℹ️ Instructions"):
        st.write("""
        - Enter your article topic.
        - Adjust the creativity if you like.
        - Click 'Generate Newsletter' to start.
        - Download the markdown result.
        """)

# --- Agent-based newsletter generation logic ---

def generate_newsletter(topic_input: str, temp: float):
    # Language model configuration
    language_model = LLM(model="command-r", temperature=temp)

    # Tool for web search
    search_utility = SerperDevTool(n_results=10)

    # Define researcher agent
    researcher = Agent(
        role="Research Strategist",
        goal=f"Conduct deep web research from reliable web sources on: {topic_input}",
        backstory=(
            "You are a highly analytical Research Strategist trained in advanced information retrieval, web scraping, and source verification. "
            "With a background in competitive intelligence and market research, your strength lies in rapidly synthesizing information from "
            "structured and unstructured sources such as news portals, research publications, and open-access datasets. You excel in validating "
            "information through triangulation, assessing source credibility using predefined heuristics, and extracting statistically significant trends. "
            "You operate with high precision under ambiguous contexts and deliver outputs that are organized, citation-rich, and insight-driven. "
            "Your findings prioritize recency, relevance, and factual reliability, enabling downstream agents to work from a high-confidence foundation."
        ),
        tools=[search_utility],
        allow_delegation=False,
        verbose=True,
        llm=language_model
    )

    # Define writer agent
    writer = Agent(
        role="Narrative Creator",
        goal="Transform research into a structured, engaging markdown article",
        backstory=(
            "You are a professional Narrative Creator with expertise in technical content design, SEO-optimized newsletter writing, and editorial storytelling. "
            "Trained in the art of translating dense research into digestible, engaging prose, you specialize in content strategies that enhance reader comprehension "
            "without diluting factual integrity. You follow a modular writing approach — crafting compelling hooks, informative sub-sections, and high-retention conclusions. "
            "You ensure seamless integration of citations using markdown formatting, maintain tone consistency, and adapt writing style to suit domain-specific audiences. "
            "Your experience spans journalism, scientific communication, and long-form content marketing. Your primary mission is to transform verified research into articles "
            "that are not only informative but also emotionally resonant and share-worthy."
        ),
        allow_delegation=False,
        verbose=True,
        llm=language_model
    )

    # Task for research
    task_research = Task(
        description="""
            Conduct a comprehensive research investigation on the topic: **{topic_input}**.
            
            Your research must incorporate the following elements:
            1. **Recent Developments** – Identify newsworthy events, product launches, regulations, or market shifts relevant to the topic from the past 6–12 months.
            2. **Macro and Micro Trends** – Analyze short-term signals and long-term patterns using data from credible industry reports, whitepapers, and academic articles.
            3. **Expert Opinions** – Extract commentary, forecasts, or critical assessments made by thought leaders, analysts, or domain experts.
            4. **Quantitative Insights** – Include key statistics, charts, or benchmarks (e.g., market size, adoption rates, funding rounds, or user growth).
            5. **Source Validation** – Prioritize high-authority, non-user-generated sources. Cross-check facts using at least two independent sources where possible.
            6. **Contextual Background** – Add historical or conceptual framing that enhances understanding of current developments.
            
            All research findings should be:
            - Structured into clearly categorized sections
            - Presented in bullet-point format for easy parsing
            - Hyperlinked to original sources in markdown `[Source](URL)` style
            - Written in plain English with brief commentary for clarity
            
            Avoid speculation or unsupported claims. Ensure factual accuracy and present only verified insights.
        """,
        expected_output="""
            A multi-section research brief including:
            - Executive Summary (3–5 key findings)
            - Categorized trends and data points
            - Direct source citations for all information
            - Insights grouped under logical themes (e.g., Technology, Market, Regulation)
            - Markdown-compatible formatting
        """,
        agent=researcher
    )


    # Task for writing
    task_write = Task(
        description="""
            Based on the structured research brief provided by the Research Strategist, your objective is to create a well-crafted, markdown-formatted newsletter article.
            
            Your deliverable should exhibit:
            1. **Narrative Structure**
               - Title: Use H1 markdown (`# Title`) that is concise and SEO-aware.
               - Introduction: Set context and articulate why the topic matters.
               - Body: Organize into thematic H3 (`###`) sections. Present key insights with clarity and flow.
               - Conclusion: Summarize implications, potential next steps, or open questions.
            
            2. **Writing Style**
               - Maintain an informative yet accessible tone; balance technical accuracy with readability.
               - Break long paragraphs into digestible chunks; use lists where appropriate.
               - Apply rhetorical techniques (e.g., analogies, transitions, parallelism) to enhance engagement.
            
            3. **Citation and Attribution**
               - Integrate hyperlinks for all facts, statistics, or quotes using `[Source](URL)` inline markdown style.
               - Include a dedicated **References** section listing all sources.
            
            4. **Markdown Compliance**
               - Ensure proper heading hierarchy (`#`, `###`)
               - Use bolding, bullet lists, and links appropriately
               - Ensure that the final output is render-ready for newsletters and newsletters and blog platforms like Medium, Ghost, or Notion.
            
            You are expected to preserve the integrity of the research findings while translating them into a compelling narrative fit for publication.
        """,
        expected_output="""
            A complete newsletter in markdown format with:
            - H1 title and multiple H3 subsections
            - Inline citations with hyperlinks to credible sources
            - Introduction and conclusion with high narrative quality
            - Reference list at the end
            - Reader-friendly formatting and natural flow
        """,
        agent=writer
    )

    # Create Crew and execute
    newsletter_crew = Crew(
        agents=[researcher, writer],
        tasks=[task_research, task_write],
        verbose=True
    )

    return newsletter_crew.kickoff(inputs={"topic_input": topic_input})


# --- Main interaction flow ---
if generate_clicked and user_topic.strip():
    with st.spinner("🧠 Thinking and writing... please wait"):
        try:
            final_output = generate_newsletter(user_topic, creativity)
            st.subheader("📝 Your AI-Generated Blog Post")
            st.markdown(final_output)

            st.download_button(
                label="📥 Download as Markdown",
                data=final_output.raw,
                file_name=f"{user_topic.strip().lower().replace(' ', '_')}.md",
                mime="text/markdown"
            )
        except Exception as err:
            st.error(f"Something went wrong: {str(err)}")

# Footer
st.markdown("---")
st.caption("Crafted with 🛠️ CrewAI + Streamlit + Cohere")

