from google.adk.agents import Agent, BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.adk.tools import google_search
from google.adk.tools.load_web_page import load_web_page
from .prompts import SEARCHER_INSTRUCTIONS, READER_INSTRUCTIONS
from typing import AsyncGenerator

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

# Custom agent to only yield reader's events
class FilteredMedicalAgent(BaseAgent):
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        # Run searcher internally but don't yield its events
        async for _ in searcher.run_async(ctx):
            pass
            
        # Run reader and yield its events to the user
        async for event in reader.run_async(ctx):
            yield event

root_agent = FilteredMedicalAgent(
    name='library_agent',
    description='Multi-step agent for comprehensive medicine information research.',
)
