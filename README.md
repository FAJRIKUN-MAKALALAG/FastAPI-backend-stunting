# Stunting Map Care Plan Backend

## 🚀 Fitur Utama

- **REST API FastAPI**: Backend berbasis FastAPI untuk kebutuhan aplikasi Stunting Map Care Plan.
- **Chatbot Gemini AI**: Endpoint untuk tanya jawab seputar stunting & gizi anak, terhubung ke Google Gemini API.
- **Analisis LLM**: Endpoint analisis kesehatan anak otomatis (LLM) setelah hitung Z-Score.
- **Integrasi Supabase**: Endpoint untuk mengirimkan Supabase URL & anon key ke frontend.
- **CORS**: Mendukung akses frontend dari domain yang diizinkan.

---

## ⚡️ Cara Kerja Integrasi Frontend

- **Supabase**:  
  Frontend **mengambil URL & anon key Supabase dari backend** melalui endpoint:
  ```
  GET /api/supabase-keys
  ```
- **Chatbot & LLM**:  
  Semua permintaan Chatbot dan LLM (analisis gizi) **dilayani oleh backend**:
  - `POST /api/chatbot`
  - `POST /api/llm-analyze`

---

## 🛠️ Cara Menjalankan Backend

### 1. **Clone & Install Dependencies**

```sh
cd backend
pip install -r requirements.txt
```

### 2. **Buat file .env**

Buat file `.env` di folder backend, isi minimal:

```
GEMINI_API_KEY=your_google_gemini_api_key
JWT_SECRET=your_jwt_secret
```

### 3. **Jalankan Server**

```sh
uvicorn main:app --reload
```

Server berjalan di `localhost:8000` (atau port lain sesuai kebutuhan).

---

## 📦 Struktur Endpoint Penting

- `/api/supabase-keys`  
  Mengirimkan Supabase URL & anon key ke frontend.
- `/api/chatbot`  
  Endpoint Chatbot Gemini AI (POST, body: `{ "message": "..." }`).
- `/api/llm-analyze`  
  Endpoint analisis LLM (POST, body: `{ "prompt": "..." }`).

---

## 📝 Catatan Pengembangan

- **Jangan hardcode credential di frontend!**  
  Semua credential Supabase & Gemini API hanya di backend.
- **CORS** sudah diatur agar frontend bisa akses backend.
- **Jika ingin ganti Supabase project**, cukup update endpoint `/api/supabase-keys` di backend.

---

## 📄 Deployment

- **Render.com**:  
  Sudah tersedia file `render.yaml` untuk deployment otomatis di Render.
- **Environment Variable**:  
  Pastikan set `GEMINI_API_KEY` di environment Render.

---

## 👩‍💻 Kontribusi

- Pastikan perubahan pada integrasi Supabase/LLM/Chatbot selalu via backend.
- Jangan hardcode credential di frontend.
