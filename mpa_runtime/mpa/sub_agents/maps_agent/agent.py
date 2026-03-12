from google.adk.agents.llm_agent import Agent
import googlemaps
import os

gmaps = googlemaps.Client(key=os.environ.get("GOOGLE_MAPS_API_KEY"))


def search_places(query: str):
    """Searches for places using the Google Maps API."""
    places_result = gmaps.places(query)
    return places_result


root_agent = Agent(
    model="gemini-2.5-flash",
    name="maps_agent",
    description="An agent that can answer questions about maps and places.",
    instruction="You are an agent that will interact with Google Maps API to answer user questions.",
    tools=[search_places],
)
