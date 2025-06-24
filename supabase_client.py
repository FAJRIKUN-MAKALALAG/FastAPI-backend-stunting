from supabase import create_client, Client
import os

# Ambil URL dan Service Key dari environment variable
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")  # Gunakan service key untuk backend

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("SUPABASE_URL dan SUPABASE_SERVICE_KEY harus di-set di environment variable!")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Contoh helper function: ambil semua data anak

def get_children():
    response = supabase.table("children").select("*").execute()
    return response.data

def get_doctors():
    response = supabase.table("profiles").select("*").eq("role", "doctor").execute()
    return response.data 