import os
import pytest
from httpx import AsyncClient
from main import app

import sys
import asyncio

# Set up event loop for Windows if needed
def pytest_configure():
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@pytest.mark.asyncio
async def test_chatbot_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/chatbot", json={"message": "Apa itu stunting?"})
        assert response.status_code == 200
        data = response.json()
        assert "reply" in data or "error" in data
        print("/api/chatbot integration: ", data)

@pytest.mark.asyncio
async def test_llm_analyze_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/llm-analyze", json={"prompt": "Analisa gizi anak usia 2 tahun"})
        assert response.status_code == 200
        data = response.json()
        assert "reply" in data or "error" in data
        print("/api/llm-analyze integration: ", data)


def test_supabase_keys():
    from main import get_supabase_keys
    keys = get_supabase_keys()
    assert "url" in keys and "anon_key" in keys
    print("/api/supabase-keys integration: ", keys) 