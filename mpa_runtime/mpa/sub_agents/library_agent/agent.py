from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
from google.adk.tools.load_web_page import load_web_page
from .prompts import SYSTEM_INSTRUCTIONS

root_agent = Agent(
    model='gemini-2.5-flash',
    name='library_agent',
    description='Agent for searching medical information from PubMed and other sources.',
    instruction=SYSTEM_INSTRUCTIONS,
    # tools=[google_search, load_web_page],
)
