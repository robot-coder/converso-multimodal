from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import httpx
from typing import List, Optional
import uuid
import os

app = FastAPI()

# Mount static files (like CSS, JS) if needed
app.mount("/static", StaticFiles(directory="static"), name="static")

# Placeholder for LLM API endpoints or configurations
LLM_API_URLS = {
    "model_a": "https://api.example.com/llm/model_a",
    "model_b": "https://api.example.com/llm/model_b"
}

# In-memory storage for conversations
conversations = {}

class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    media_url: Optional[str] = None

class Conversation(BaseModel):
    id: str
    theme: Optional[str] = None
    messages: List[Message] = []

@app.get("/", response_class=HTMLResponse)
async def get_index():
    """
    Serve the main HTML page.
    """
    with open("index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/start_conversation/")
async def start_conversation(theme: Optional[str] = Form(None)):
    """
    Initialize a new conversation with an optional theme.
    """
    conv_id = str(uuid.uuid4())
    conversations[conv_id] = Conversation(id=conv_id, theme=theme, messages=[])
    return {"conversation_id": conv_id}

@app.post("/send_message/")
async def send_message(
    conversation_id: str = Form(...),
    message: str = Form(...),
    model_choice: str = Form("model_a"),
    media: Optional[UploadFile] = File(None)
):
    """
    Handle user message, optional media upload, and generate assistant response.
    """
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    conv = conversations[conversation_id]

    media_url = None
    if media:
        try:
            media_filename = f"media/{uuid.uuid4()}_{media.filename}"
            os.makedirs(os.path.dirname(media_filename), exist_ok=True)
            with open(media_filename, "wb") as buffer:
                buffer.write(await media.read())
            media_url = f"/{media_filename}"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Media upload failed: {str(e)}")

    # Append user message
    conv.messages.append(Message(role="user", content=message, media_url=media_url))

    # Prepare prompt for LLM
    prompt = ""
    for msg in conv.messages:
        role = "User" if msg.role == "user" else "Assistant"
        prompt += f"{role}: {msg.content}\n"
    # Call LLM API
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                LLM_API_URLS.get(model_choice, LLM_API_URLS["model_a"]),
                json={"prompt": prompt}
            )
            response.raise_for_status()
            llm_response = response.json().get("response", "")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"LLM API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    # Append assistant response
    conv.messages.append(Message(role="assistant", content=llm_response))

    return {
        "response": llm_response,
        "conversation_id": conversation_id
    }

@app.get("/get_conversation/")
async def get_conversation(conversation_id: str):
    """
    Retrieve the full conversation history.
    """
    conv = conversations.get(conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv

@app.post("/compare_models/")
async def compare_models(
    message: str = Form(...),
    models: List[str] = Form(...)
):
    """
    Send the same message to multiple models for comparison.
    """
    responses = {}
    for model in models:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    LLM_API_URLS.get(model, LLM_API_URLS["model_a"]),
                    json={"prompt": message}
                )
                resp.raise_for_status()
                responses[model] = resp.json().get("response", "")
        except httpx.HTTPError:
            responses[model] = "Error fetching response"
    return responses

@app.post("/upload_media/")
async def upload_media(file: UploadFile = File(...)):
    """
    Handle media uploads separately if needed.
    """
    try:
        filename = f"media/{uuid.uuid4()}_{file.filename}"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "wb") as buffer:
            buffer.write(await file.read())
        return {"media_url": f"/{filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Media upload failed: {str(e)}")