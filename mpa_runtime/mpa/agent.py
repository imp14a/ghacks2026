from google.adk.agents.llm_agent import Agent
from google.adk.agents.callback_context import CallbackContext
from .sub_agents.maps_agent.agent import root_agent as maps_agent
from .sub_agents.inventory_agent.agent import root_agent as inventory_agent
from .sub_agents.calendar_agent.agent import root_agent as calendar_agent
from .sub_agents.library_agent.agent import root_agent as library_agent
from google.genai import types
from typing import Optional


from .prompts import SYSTEM_INSTRUCTIONS


def before_agent_callback_load_file(callback_context: CallbackContext) -> Optional[types.Content]:
    print("before_agent_callback_load_file")
    print(f"{callback_context}")
    pass


root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="Medical Prescription Orchestrator",
    instruction=SYSTEM_INSTRUCTIONS,
    sub_agents=[
        maps_agent,
        inventory_agent,
        calendar_agent,
        library_agent,
    ],
    before_agent_callback=before_agent_callback_load_file,
)
