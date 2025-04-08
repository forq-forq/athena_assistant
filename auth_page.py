import streamlit as st
import re
from auth import register_user, login_user, get_user_role


def authentication_ui():
    st.title("🔐 Athena Assistant Login")

    if st.session_state.get("force_switch_to_login"):
        st.session_state["force_switch_to_login"] = False
        st.session_state["auth_mode"] = "Login"
        st.rerun()

    mode = st.radio("Choose mode:", ["Login", "Register"], key="auth_mode")

    allowed_domain = "athena.com"

    if mode == "Register":
        email = st.text_input("Email", key="email_register")
        password = st.text_input("Password", type="password", key="password_register")

        if st.button("Sign up"):
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                st.error("❌ Invalid email format")
            elif not email.lower().endswith(f"@{allowed_domain}"):
                st.error(f"❌ Registration is available only for email addresses @{allowed_domain}")
            elif len(password) < 6:
                st.error("❌ Password must contain at least 6 characters")
            else:
                res = register_user(email, password)
                try:
                    data = res.json()
                except Exception:
                    data = {}

                if res.status_code >= 400 or "error" in data:
                    message = (
                        data.get("error", {}).get("message") or
                        data.get("msg") or
                        f"Error's code: {res.status_code}"
                    )
                    if "User already registered" in str(message):
                        st.error("❌ User with such email already exists")
                    else:
                        st.error(f"❌ Registration error: {message}")
                else:
                    st.success("✅ Registration has been done successfully. Login to account.")
                    st.session_state["force_switch_to_login"] = True
                    st.rerun()


    else:
        email = st.text_input("Email", key="log_email")
        password = st.text_input("Password", type="password", key="log_password")

        if st.button("Sign in"):
            response = login_user(email, password)
            if "access_token" in response:
                st.session_state["user"] = response.get("user", {})
                st.session_state["token"] = response["access_token"]
                role = get_user_role(st.session_state["user"]["id"])
                st.session_state["role"] = role or "user"
                st.success("✅ Sign in has been done successfully.!")
                st.rerun()
            elif "error" in response:
                st.error(f"❌ Sign in error: {response['error']['message']}")
            else:
                st.error("❌ Failed to sign in. Please check your details.")
