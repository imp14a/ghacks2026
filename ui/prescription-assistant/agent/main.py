"""Prescription Assistant feature."""

from __future__ import annotations

import json
from typing import Dict, Optional

from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from dotenv import load_dotenv
from fastapi import FastAPI
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.tools import ToolContext
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()


class PrescriptionState(BaseModel):
    """List of the prescriptions being managed."""

    prescriptions: list[str] = Field(
        default_factory=list,
        description="The list of already recorded prescriptions",
    )


def set_prescriptions(tool_context: ToolContext, new_prescriptions: list[str]) -> Dict[str, str]:
    """
    Set the list of prescriptions using the provided new list.

    Args:
        "new_prescriptions": {
            "type": "array",
            "items": {"type": "string"},
            "description": "The new list of prescriptions to maintain",
        }

    Returns:
        Dict indicating success status and message
    """
    try:
        # Put this into a state object just to confirm the shape
        new_state = {"prescriptions": new_prescriptions}
        tool_context.state["prescriptions"] = new_state["prescriptions"]
        return {"status": "success", "message": "Prescriptions updated successfully"}

    except Exception as e:
        return {"status": "error", "message": f"Error updating prescriptions: {str(e)}"}


def get_weather(tool_context: ToolContext, location: str) -> Dict[str, str]:
    """Get the weather for a given location. Ensure location is fully spelled out."""
    return {"status": "success", "message": f"The weather in {location} is sunny."}


def on_before_agent(callback_context: CallbackContext):
    """
    Initialize prescriptions state if it doesn't exist.
    """

    if "prescriptions" not in callback_context.state:
        # Initialize with default prescription
        default_prescriptions = ["Aspirin - 100mg - Daily"]
        callback_context.state["prescriptions"] = default_prescriptions

    return None


# --- Define the Callback Function ---
#  modifying the agent's system prompt to incude the current state of the prescriptions list
def before_model_modifier(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """Inspects/modifies the LLM request or skips the call."""
    agent_name = callback_context.agent_name
    if agent_name == "PrescriptionAgent":
        prescriptions_json = "No prescriptions yet"
        if (
            "prescriptions" in callback_context.state
            and callback_context.state["prescriptions"] is not None
        ):
            try:
                prescriptions_json = json.dumps(callback_context.state["prescriptions"], indent=2)
            except Exception as e:
                prescriptions_json = f"Error serializing prescriptions: {str(e)}"
        # --- Modification Example ---
        # Add a prefix to the system instruction
        original_instruction = llm_request.config.system_instruction or types.Content(
            role="system", parts=[]
        )
        prefix = f"""You are a helpful assistant for maintaining a list of prescriptions.
        This is the current state of the list of prescriptions: {prescriptions_json}
        When you modify the list of prescriptions (whether to add, remove, or modify one or more prescriptions), use the set_prescriptions tool to update the list."""
        # Ensure system_instruction is Content and parts list exists
        if not isinstance(original_instruction, types.Content):
            # Handle case where it might be a string (though config expects Content)
            original_instruction = types.Content(
                role="system", parts=[types.Part(text=str(original_instruction))]
            )
        if not original_instruction.parts:
            original_instruction.parts = [types.Part(text="")]

        # Modify the text of the first part
        if original_instruction.parts and len(original_instruction.parts) > 0:
            modified_text = prefix + (original_instruction.parts[0].text or "")
            original_instruction.parts[0].text = modified_text
        llm_request.config.system_instruction = original_instruction

    return None


# --- Define the Callback Function ---
def simple_after_model_modifier(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
    """Stop the consecutive tool calling of the agent"""
    agent_name = callback_context.agent_name
    # --- Inspection ---
    if agent_name == "PrescriptionAgent":
        if llm_response.content and llm_response.content.parts:
            # Assuming simple text response for this example
            if (
                llm_response.content.role == "model"
                and llm_response.content.parts[0].text
            ):
                callback_context._invocation_context.end_invocation = True

        elif llm_response.error_message:
            return None
        else:
            return None  # Nothing to modify
    return None


prescription_agent = LlmAgent(
    name="PrescriptionAgent",
    model="gemini-2.5-flash",
    instruction="""
        You are a helpful assistant for maintaining a list of prescriptions.
        
        When a user uploads an image (like a photo of a prescription bottle or a paper prescription), you MUST:
        1. Analyze the image to identify the medication name, dosage (e.g., 500mg), and frequency/instructions.
        2. Extract this information and suggest adding it to the prescription list.
        3. Use the set_prescriptions tool to update the list if the user confirms or if they asked you to "Add this".

        When a user asks you to do anything regarding prescriptions, you MUST use the set_prescriptions tool.

        IMPORTANT RULES ABOUT PRESCRIPTIONS AND THE SET_PRESCRIPTIONS TOOL:
        1. Always use the set_prescriptions tool for any prescriptions-related requests
        2. Always pass the COMPLETE LIST of prescriptions to the set_prescriptions tool. If the list had 5 prescriptions and you removed one, you must pass the complete list of 4 remaining prescriptions.
        3. You can use existing prescriptions if one is relevant to the user's request, but you can also create new prescriptions as required.
        4. Be helpful in managing prescriptions, providing clear names, dosages, and frequencies.
        5. After using the tool, provide a brief summary of what you create, removed, or changed.

        Examples of when to use the set_prescriptions tool:
        - "Add a prescription for Ibuprofen 400mg twice a day" → Use tool with an array containing the existing list of prescriptions with the new prescription at the end.
        - "Remove my Aspirin" → Use tool with an array containing all of the existing prescriptions except the Aspirin one.
        - "Change the dose of my Aspirin to 75mg" → Use tool with an array of all of the prescriptions, with the Aspirin one modified.

        Do your best to ensure prescriptions plausibly make sense.


        IMPORTANT RULES ABOUT WEATHER AND THE GET_WEATHER TOOL:
        1. Only call the get_weather tool if the user asks you for the weather in a given location.
        2. If the user does not specify a location, you can use the location "Everywhere ever in the whole wide world"
        """,
    tools=[set_prescriptions, get_weather],
    before_agent_callback=on_before_agent,
    before_model_callback=before_model_modifier,
    after_model_callback=simple_after_model_modifier,
)

# Create ADK middleware agent instance
adk_prescription_agent = ADKAgent(
    adk_agent=prescription_agent,
    user_id="demo_user",
    session_timeout_seconds=3600,
    use_in_memory_services=True,
)

# Create FastAPI app
app = FastAPI(title="ADK Middleware Prescription Assistant")

# Add the ADK endpoint
add_adk_fastapi_endpoint(app, adk_prescription_agent, path="/")

if __name__ == "__main__":
    import os

    import uvicorn

    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  Warning: GOOGLE_API_KEY environment variable not set!")
        print("   Set it with: export GOOGLE_API_KEY='your-key-here'")
        print("   Get a key from: https://makersuite.google.com/app/apikey")
        print()

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
