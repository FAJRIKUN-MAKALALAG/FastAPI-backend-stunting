import os
from fastapi import FastAPI, Request, Path, HTTPException, Header, Depends

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import httpx
import re
from supabase_client import (
    get_children, get_doctors,
    insert_child, update_child, delete_child,
    get_notifications, insert_notification, mark_notification_read, delete_notification, mark_all_notifications_read, delete_all_notifications, supabase
)
import jwt

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

@app.get("/api/children")
def read_children():
    try:
        data = get_children()
        return JSONResponse({"data": data})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/api/doctors")
def read_doctors():
    try:
        data = get_doctors()
        return JSONResponse({"data": data})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/api/children")
def create_child(child: dict):
    try:
        data = insert_child(child)
        return JSONResponse({"data": data})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.patch("/api/children/{child_id}")
def patch_child(child_id: str, update: dict):
    try:
        data = update_child(child_id, update)
        return JSONResponse({"data": data})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.delete("/api/children/{child_id}")
def remove_child(child_id: str):
    try:
        data = delete_child(child_id)
        return JSONResponse({"data": data})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# NOTIFICATIONS
@app.get("/api/notifications")
def read_notifications():
    try:
        data = get_notifications()
        return JSONResponse({"data": data})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/api/notifications")
def create_notification(notif: dict):
    try:
        data = insert_notification(notif)
        return JSONResponse({"data": data})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.patch("/api/notifications/{notif_id}/read")
def patch_notification_read(notif_id: str):
    try:
        data = mark_notification_read(notif_id)
        return JSONResponse({"data": data})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.delete("/api/notifications/{notif_id}")
def remove_notification(notif_id: str):
    try:
        data = delete_notification(notif_id)
        return JSONResponse({"data": data})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.patch("/api/notifications/read-all")
def patch_all_notifications_read():
    try:
        data = mark_all_notifications_read()
        return JSONResponse({"data": data})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.delete("/api/notifications")
def remove_all_notifications():
    try:
        data = delete_all_notifications()
        return JSONResponse({"data": data})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/api/supabase-status")
def supabase_status():
    try:
        # Cek koneksi dengan query sederhana
        data = get_children()
        return JSONResponse({"status": "ok", "message": "Supabase connected", "sample": data[:1] if data else []})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

# Helper untuk ambil user dari Supabase
def get_user_by_email(email):
    response = supabase.table("profiles").select("*").eq("email", email).single().execute()
    return response.data

def verify_password(plain, hashed):
    # Untuk demo, password disimpan plain (tidak direkomendasikan untuk production!)
    return plain == hashed

# Endpoint login
class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/api/login")
def login(request: LoginRequest):
    user = get_user_by_email(request.email)
    if not user or not verify_password(request.password, user.get("password")):
        raise HTTPException(status_code=401, detail="Email atau password salah")
    # Buat JWT token
    token = jwt.encode({"user_id": user["id"], "email": user["email"]}, JWT_SECRET, algorithm=JWT_ALGO)
    return {"token": token, "user": {"id": user["id"], "email": user["email"], "role": user.get("role")}}

# Dependency untuk auth
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGO])
        user = get_user_by_email(payload["email"])
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Token tidak valid")

@app.get("/api/me")
def me(user=Depends(get_current_user)):
    return {"id": user["id"], "email": user["email"], "role": user.get("role")} 