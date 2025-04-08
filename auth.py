import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

HEADERS = {
    "apikey": SUPABASE_API_KEY,
    "Content-Type": "application/json"
}

def register_user(email, password):
    url = f"{SUPABASE_URL}/auth/v1/signup"
    payload = {"email": email, "password": password}
    res = requests.post(url, json=payload, headers=HEADERS)

    if res.status_code == 200:
        data = res.json()
        user_id = data.get("user", {}).get("id")

        if user_id:
            profile_payload = {
                "id": user_id,
                "email": email,
                "role": "user"
            }
            profile_url = f"{SUPABASE_URL}/rest/v1/user_profiles"
            requests.post(profile_url, json=profile_payload, headers={**HEADERS, "Content-Type": "application/json"})

    return res

def login_user(email, password):
    url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"
    payload = {"email": email, "password": password}
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()

def get_user_role(user_id):
    url = f"{SUPABASE_URL}/rest/v1/user_profiles?id=eq.{user_id}&select=role"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200 and res.json():
        return res.json()[0]["role"]
    return None