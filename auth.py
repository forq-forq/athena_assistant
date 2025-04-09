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
                "role": "user",
                "email": email
            }
            profile_url = f"{SUPABASE_URL}/rest/v1/user_profile"
            requests.post(profile_url, json=profile_payload, headers={**HEADERS, "Content-Type": "application/json"})

    return res

def login_user(email, password):
    url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"
    payload = {"email": email, "password": password}
    headers = {**HEADERS, "Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    if "access_token" not in data:
        return data

    user_id = data.get("user", {}).get("id")
    if not user_id:
        user_res = requests.get(
            f"{SUPABASE_URL}/auth/v1/user",
            headers={"Authorization": f"Bearer {data['access_token']}", "apikey": SUPABASE_API_KEY}
        )
        user_data = user_res.json()
        user_id = user_data.get("id")

    profile_res = requests.get(
        f"{SUPABASE_URL}/rest/v1/user_profile?id=eq.{user_id}&select=*",
        headers=headers
    )
    profiles = profile_res.json()

    if not profiles:
        profile_payload = {
            "id": user_id,
            "email": email,
            "role": "user"
        }
        create_res = requests.post(
            f"{SUPABASE_URL}/rest/v1/user_profile",
            json=profile_payload,
            headers=headers
        )
        print(f"📥 Created user profile: {create_res.status_code}")

    data["user"] = {
        "id": user_id,
        "email": email
    }

    return data


def get_user_role(user_id):
    if not user_id:
        return None

    url = f"{SUPABASE_URL}/rest/v1/user_profile?id=eq.{user_id}&select=role"
    res = requests.get(url, headers=HEADERS)

    if res.status_code == 200 and res.json():
        return res.json()[0].get("role")

    return None