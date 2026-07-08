import streamlit as st
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def initialize_session_state():
    """Initialize session state variables"""
    if "user" not in st.session_state:
        st.session_state["user"] = None
    if "auth_mode" not in st.session_state:
        st.session_state["auth_mode"] = "Login"
    if "session" not in st.session_state:
        st.session_state["session"] = None
    if "df" not in st.session_state:
        st.session_state["df"] = None
    if "is_paid" not in st.session_state:
        st.session_state["is_paid"] = False
    if "page" not in st.session_state:
        st.session_state["page"] = "Dashboard"

def login_user(email, password):
    """Authenticate user with email and password"""
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        st.session_state["user"] = email
        st.session_state["session"] = res.session
        st.success("✅ Login successful!")
        st.rerun()
    except Exception as e:
        st.error(f"❌ {str(e)}")

def signup_user(email, password):
    """Register a new user"""
    try:
        supabase.auth.sign_up({"email": email, "password": password})
        st.success("✅ Account created successfully!")
        st.session_state["auth_mode"] = "Login"
        st.rerun()
    except Exception as e:
        st.error(f"❌ {str(e)}")

def logout_user():
    """Log out the current user"""
    st.session_state["user"] = None
    st.session_state["session"] = None
    st.rerun()
