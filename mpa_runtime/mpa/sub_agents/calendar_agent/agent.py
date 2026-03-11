from google.adk.agents.llm_agent import Agent
from .prompts import SYSTEM_INSTRUCTIONS

from google.adk.tools.google_api_tool.google_api_toolset import GoogleApiToolset
import os
import datetime

from tzlocal import get_localzone

def get_today_date():
    return datetime.date.today().isoformat()


def get_timezone():
    return str(get_localzone())

root_agent = Agent(
    model='gemini-2.5-flash',
    name='calendar_agent',
    description='Agent for managing calendar events',
    instruction=SYSTEM_INSTRUCTIONS,
    tools=[get_today_date, get_timezone, GoogleApiToolset(
        api_name="calendar",
        api_version="v3",
        client_id=os.getenv("GOOGLE_CLIENT_ID","969700488226-raf9b2h0oao9q8p5f63sstbpgmkdimke.apps.googleusercontent.com"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET","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"),
        
    )],
)
