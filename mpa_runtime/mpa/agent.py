from google.adk.agents.llm_agent import Agent
from google.adk.agents.callback_context import CallbackContext
from .sub_agents.maps_agent.agent import root_agent as maps_agent
from .sub_agents.inventory_agent.agent import root_agent as inventory_agent
from .sub_agents.calendar_agent.agent import root_agent as calendar_agent
from .sub_agents.library_agent.agent import root_agent as library_agent
from google.cloud import storage
from google.genai import types
from typing import Optional


from .prompts import SYSTEM_INSTRUCTIONS


def before_agent_callback_load_file(callback_context: CallbackContext) -> Optional[types.Content]:
    # Check if one part of parts contains the gcs text, if yes, we need to split this into two messages one with the text and other with the url
    new_parts = []
    for part in callback_context.user_content.parts:
        if part.text and "gs://" in part.text:
            # Extract the URI and any surrounding text
            text_content = part.text
            import re

            uri_match = re.search(r"gs://[^\s]+", text_content)
            if uri_match:
                gcs_uri = uri_match.group(0)
                # Add the text part without the URI if there's other text
                remaining_text = text_content.replace(gcs_uri, "").strip()
                if remaining_text:
                    new_parts.append(types.Part.from_text(text=remaining_text))

                # Extract the file content from GCS
                storage_client = storage.Client()
                bucket_name = gcs_uri.split("/")[2]
                blob_name = "/".join(gcs_uri.split("/")[3:])
                bucket = storage_client.bucket(bucket_name)
                blob = bucket.blob(blob_name)
                file_bytes = blob.download_as_bytes()

                new_parts.append(types.Part.from_bytes(data=file_bytes, mime_type="image/jpeg"))
                continue
        new_parts.append(part)

    if new_parts:
        callback_context.user_content.parts = new_parts

    return None


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
