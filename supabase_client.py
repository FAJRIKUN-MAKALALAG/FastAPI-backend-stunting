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

def insert_child(child_data):
    response = supabase.table("children").insert(child_data).execute()
    return response.data

def update_child(child_id, update_data):
    response = supabase.table("children").update(update_data).eq("id", child_id).execute()
    return response.data

def delete_child(child_id):
    response = supabase.table("children").delete().eq("id", child_id).execute()
    return response.data

# NOTIFICATIONS

def get_notifications(filters=None):
    query = supabase.table("notifications").select("*")
    if filters:
        for key, value in filters.items():
            query = query.eq(key, value)
    response = query.execute()
    return response.data

def insert_notification(notif_data):
    response = supabase.table("notifications").insert(notif_data).execute()
    return response.data

def mark_notification_read(notif_id):
    response = supabase.table("notifications").update({"is_read": True}).eq("id", notif_id).execute()
    return response.data

def delete_notification(notif_id):
    response = supabase.table("notifications").delete().eq("id", notif_id).execute()
    return response.data

def mark_all_notifications_read():
    response = supabase.table("notifications").update({"is_read": True}).execute()
    return response.data

def delete_all_notifications():
    response = supabase.table("notifications").delete().execute()
    return response.data 