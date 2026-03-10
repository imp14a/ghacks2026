

from google.adk.agents.llm_agent import Agent
from google.adk.tools.function_tool import FunctionTool as Tool
import googlemaps
import os

gmaps = googlemaps.Client(key=os.environ.get('GOOGLE_MAPS_API_KEY'))

def search_places(query: str):
  """Searches for places using the Google Maps API."""
  places_result = gmaps.places(query)
  return places_result

places_search_tool = Tool(
    name='places_search',
    description='Search for a place.',
    func=search_places,
)

maps_agent = Agent(
    model='gemini-2.5-flash',
    name='maps_agent',
    description='An agent that can answer questions about maps and places.',
    instruction='You are an agent that will interact with Google Maps API to answer user questions.',
    tools=[places_search_tool],
)
