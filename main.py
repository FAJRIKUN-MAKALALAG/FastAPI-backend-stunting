import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import httpx

load_dotenv()

app = FastAPI()

# Allow CORS for local dev and Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY

@app.post("/api/chatbot")
async def chatbot_endpoint(request: ChatRequest):
    if not GEMINI_API_KEY:
        return JSONResponse({"error": "Gemini API key not set."}, status_code=500)
    payload = {
        "contents": [
            {"parts": [{"text": request.message}]}
        ]
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(GEMINI_API_URL, json=payload, timeout=20)
            response.raise_for_status()
            data = response.json()
            # Ambil respons teks dari Gemini
            reply = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "[No response]")
            return JSONResponse({"reply": reply})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500) 