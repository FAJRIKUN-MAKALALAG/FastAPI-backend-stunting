import os
from fastapi import FastAPI, Request, Path, HTTPException, Header, Depends

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import httpx
import re


# Paksa path ke file .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


app = FastAPI()

# Allow CORS for local dev and Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://stuntingcaresulut.domcloud.dev/",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",        # tambahkan ini
        "http://127.0.0.1:8080"         # dan ini
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class AnalyzeRequest(BaseModel):
    prompt: str

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY

JWT_SECRET = os.getenv("JWT_SECRET", "secret-key-anda")
JWT_ALGO = "HS256"

def clean_and_shorten_reply(text: str, max_sentences: int = 4) -> str:
    # Hilangkan simbol **, ##, --, *, #, dan spasi di awal baris
    text = re.sub(r"(\*\*|##|--|\*|#)", "", text)
    text = re.sub(r"^\s+", "", text, flags=re.MULTILINE)
    # Hilangkan spasi berlebih
    text = re.sub(r"\s+", " ", text).strip()
    # Potong maksimal max_sentences kalimat
    sentences = re.split(r"(?<=[.!?]) +", text)
    short_sentences = [s.strip() for s in sentences[:max_sentences] if s.strip()]
    # Gabungkan dengan baris baru agar mudah dibaca
    short_text = "\n".join(short_sentences)
    return short_text

@app.post("/api/chatbot")
async def chatbot_endpoint(request: ChatRequest):
    if not GEMINI_API_KEY:
        return JSONResponse({"error": "Gemini API key not set."}, status_code=500)
    # Sistem prompt untuk membatasi topik
    system_prompt = (
        "Anda adalah asisten ahli gizi anak dan pencegahan stunting. "
        "Jawab hanya pertanyaan seputar gizi anak dan stunting. "
        "Jika ada pertanyaan di luar topik, balas dengan: 'Maaf, saya hanya dapat membantu seputar gizi anak dan stunting.'"
    )
    # Gabungkan sistem prompt dengan pesan user
    full_message = f"{system_prompt}\n\nPertanyaan user: {request.message}"
    payload = {
        "contents": [
            {"parts": [{"text": full_message}]}
        ]
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(GEMINI_API_URL, json=payload, timeout=20)
            response.raise_for_status()
            data = response.json()
            reply = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "[No response]")
            reply = clean_and_shorten_reply(reply)
            return JSONResponse({"reply": reply})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/api/llm-analyze")
async def llm_analyze_endpoint(request: AnalyzeRequest):
    if not GEMINI_API_KEY:
        return JSONResponse({"error": "Gemini API key not set."}, status_code=500)
    payload = {
        "contents": [
            {"parts": [{"text": request.prompt}]}
        ]
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(GEMINI_API_URL, json=payload, timeout=20)
            response.raise_for_status()
            data = response.json()
            reply = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "[No response]")
            reply = clean_and_shorten_reply(reply)
            return JSONResponse({"reply": reply})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/api/supabase-keys")
def get_supabase_keys():
    return {
        "url": "https://sadtnyksdiujxgvwxspc.supabase.co",  # Ganti dengan URL Supabase Anda
        "anon_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNhZHRueWtzZGl1anhndnd4c3BjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk2NDI3MzYsImV4cCI6MjA2NTIxODczNn0.DbQczBTxQSAVS03DZYYqwO3_isT8cRMTvHLfQFwhkec"                   # Ganti dengan anon key Supabase Anda
    }