import streamlit as st
from dotenv import load_dotenv
from auth_page import authentication_ui

st.set_page_config(page_title="Athena AI Assistant", layout="centered")

load_dotenv()

if "user" not in st.session_state:
    authentication_ui()
    st.stop()


else:
    role = st.session_state.get("role", "user")

    if role == "admin":
        from admin_page import admin_ui
        admin_ui()
    else:
        from user_page import user_ui
        user_ui()

if st.session_state.get("role") == "admin":
    st.sidebar.success("🔒 Admin mode")
else:
    st.sidebar.info("👤 User mode")

st.sidebar.write(f"👤 You entered as: {st.session_state['user'].get('email', 'Unknown user')}")
if st.sidebar.button("🚪 Exit"):
    st.session_state.clear()
    st.rerun()
