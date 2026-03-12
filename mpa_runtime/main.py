"""Prescription Assistant feature."""

from __future__ import annotations
from dotenv import load_dotenv

load_dotenv()

import os
import uuid
from google.cloud import storage
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mpa.agent import root_agent


# Create ADK middleware agent instance
adk_prescription_agent = ADKAgent(
    adk_agent=root_agent,
    user_id="demo_user",
    session_timeout_seconds=3600,
    use_in_memory_services=True,
)

# Create FastAPI app
app = FastAPI(title="ADK Middleware Prescription Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add the ADK endpoint
add_adk_fastapi_endpoint(app, adk_prescription_agent, path="/")


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    try:
        storage_client = storage.Client()
        bucket_name = "ghacks2026-argo-team-presciptions-iamges"
        bucket = storage_client.bucket(bucket_name)

        # Generate a unique filename to avoid overwrites
        blob_name = f"{uuid.uuid4()}-{file.filename}"
        blob = bucket.blob(blob_name)

        # Upload the file content
        content = await file.read()
        blob.upload_from_string(content, content_type=file.content_type)

        return {
            "filename": f"gs://{bucket_name}/{blob_name}",
            "message": "File uploaded successfully to Google Cloud Storage",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import os

    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
