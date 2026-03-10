from google.adk.agents.llm_agent import Agent
from mpa.sub_agents.maps_agent import maps_agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    sub_agents=[
        maps_agent,
    ],
)
