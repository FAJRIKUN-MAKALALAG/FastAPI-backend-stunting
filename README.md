# Stunting Map Care Plan Backend

## 📋 Functional Requirements

- Menyediakan REST API untuk frontend (FastAPI).
- Endpoint untuk login, register, dan autentikasi user (jika ada).
- Endpoint untuk Chatbot Gemini AI (`/api/chatbot`).
- Endpoint untuk analisis LLM (`/api/llm-analyze`).
- Endpoint untuk mengirimkan Supabase URL & anon key ke frontend (`/api/supabase-keys`).
- Validasi dan sanitasi input dari frontend.
- Mendukung CORS untuk domain frontend yang diizinkan.
- Menyimpan dan mengambil data anak, status gizi, dan notifikasi (jika ada endpoint terkait).
- Menghitung Z-Score dan status gizi anak (jika dilakukan di backend).
- Menyediakan notifikasi otomatis jika status gizi/stunting berisiko (jika ada logic di backend).

## 📋 Non-Functional Requirements

- Backend harus berjalan stabil dan responsif (FastAPI, async endpoint).
- Semua credential (Supabase, Gemini API) hanya disimpan di backend, tidak di frontend.
- Mendukung deployment di Render.com dan server lokal.
- Mendukung testing (unit/integration) untuk endpoint utama.
- Kode harus menggunakan Python 3.9+ dan dependency yang jelas di `requirements.txt`.
- Dokumentasi endpoint dan setup harus jelas di README.
- Mendukung CORS dan keamanan API (JWT, dsb jika ada).
- Error handling yang baik dan logging error ke console/server.
- Tidak ada credential sensitif di repo (gunakan .env).

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
uvicorn main:app --host 0.0.0.0 --port 8000
```

Server berjalan di `localhost:8000` (atau port lain sesuai kebutuhan).

---

## 🧪 Cara Menjalankan Test Backend

### 1. **Aktifkan Virtual Environment (Opsional)**

Jika menggunakan virtual environment, aktifkan dulu:

Windows:

```sh
venv\Scripts\activate
```

Linux/Mac:

```sh
source venv/bin/activate
```

### 2. **Install Dependensi**

Pastikan sudah install dependensi:

```sh
pip install -r requirements.txt
```

### 3. **Jalankan Test dengan pytest**

Untuk menjalankan seluruh test (termasuk test_integration.py):

```sh
pytest
```

Atau hanya file tertentu:

```sh
pytest test_integration.py
```

Jika semua test berhasil, akan muncul pesan seperti:

```
test_integration.py ... [100%]
```

Jika ada warning Deprecation (misal terkait FastAPI), test tetap berjalan selama statusnya PASSED.

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

... fajrikun
