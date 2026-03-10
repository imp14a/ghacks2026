from google.adk.agents.llm_agent import Agent
from .sub_agents.maps_agent.agent import root_agent as maps_agent

from .prompts import SYSTEM_INSTRUCTIONS

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Medical Prescription Orchestrator',
    instruction=SYSTEM_INSTRUCTIONS,
    sub_agents=[
        maps_agent,
    ],
)
