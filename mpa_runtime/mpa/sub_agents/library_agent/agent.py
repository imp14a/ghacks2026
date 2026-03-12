from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import google_search
from google.adk.tools.load_web_page import load_web_page
from .prompts import SEARCHER_INSTRUCTIONS, READER_INSTRUCTIONS

# 1. Searcher (Uses Google Search built-in tool)
searcher = Agent(
    model='gemini-2.5-flash',
    name='medical_searcher',
    description='Finds PubMed and other medical articles about medicines.',
    instruction=SEARCHER_INSTRUCTIONS,
    tools=[google_search],
    output_key="search_results" # Store findings for the Reader
)

# 2. Reader (Uses Function Calling for loading pages)
reader = Agent(
    model='gemini-2.5-flash',
    name='medical_reader',
    description='Analyzes and summarizes the content of found medical URLs.',
    instruction=READER_INSTRUCTIONS + "\nUse the search results from the previous step: {search_results}",
    tools=[load_web_page],
)

# Root agent is now a Sequence of these two steps
root_agent = SequentialAgent(
    name='library_agent',
    description='Multi-step agent for comprehensive medicine information research.',
    sub_agents=[searcher, reader],
)
