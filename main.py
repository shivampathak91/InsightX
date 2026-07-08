import streamlit as st

# Page Configuration - Must be first Streamlit command
st.set_page_config(
    page_title="InSightX - AI Retail Intelligence",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
from datetime import datetime
import warnings
import base64
import os
warnings.filterwarnings('ignore')

# Encode logo as base64 for use in HTML
def get_base64_logo():
    # Try different paths to find logo.png
    paths_to_try = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo2.png"),
        "logo.png",
        "logo2.png"
    ]
    for path in paths_to_try:
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    data = base64.b64encode(f.read()).decode()
                return f"data:image/png;base64,{data}"
            except Exception:
                pass
    return ""

LOGO_BASE64 = get_base64_logo()

# Import from modular files
from config import SUPABASE_URL, SUPABASE_KEY, GROQ_API_KEY
from auth import initialize_session_state, login_user, signup_user, logout_user
from ai_functions import generate_executive_summary, ai_explain
from ui_components import create_premium_card

# Import page renderers
from page_modules.dashboard import render_dashboard
from page_modules.analytics import render_analytics
from page_modules.forecast import render_forecast
from page_modules.anomaly_detection import render_anomaly_detection
from page_modules.recommendations import render_recommendations
from page_modules.business_health import render_business_health
from page_modules.ai_assistant import render_ai_assistant
from page_modules.reports import render_reports

# ================= INITIALIZE STATE =================
initialize_session_state()

# Check for query parameter from payment checkout
if "payment_success" in st.query_params and st.query_params["payment_success"] == "true":
    st.session_state["is_paid"] = True
    st.session_state["show_success_toast"] = True
    st.query_params.clear()
    st.rerun()

# Inline render the checkout page if requested via state or query param
if st.query_params.get("page") == "premium" or st.session_state.get("page") == "premium":
    from page_modules.premium_checkout import render_premium_checkout
    render_premium_checkout()
    st.stop()

# Background polling for localStorage removed due to iframe sandboxing restrictions

# Auto-load demo dataset (superstore.csv) if logged in and df is not set
if st.session_state.get("user") and st.session_state.get("df") is None:
    demo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "superstore.csv")
    if os.path.exists(demo_path):
        try:
            demo_df = pd.read_csv(demo_path, encoding='latin1')
            demo_df.columns = demo_df.columns.str.lower()
            st.session_state["df"] = demo_df
        except Exception:
            pass

# ================= LOGIN UI =================
if not st.session_state["user"]:
    # Custom CSS for full viewport height responsive layout
    st.markdown("""
    <style>
        /* General App Background */
        .stApp { 
            background-color: #060913 !important; 
            background-image: radial-gradient(circle at 15% 85%, rgba(67, 30, 201, 0.15) 0%, transparent 40%),
                              radial-gradient(circle at 85% 15%, rgba(67, 30, 201, 0.05) 0%, transparent 40%);
            color: #FFFFFF;
            font-family: 'Inter', sans-serif;
        }
        
        /* Hide top header and sidebar completely */
        header {visibility: hidden;}
        [data-testid="stSidebar"], 
        section[data-testid="stSidebar"], 
        .stSidebar,
        [data-testid="stSidebarCollapsedControl"],
        div[data-testid="stSidebarCollapseButton"],
        button[kind="header"] {
            display: none !important;
            width: 0px !important;
            height: 0px !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        section[data-testid="stMainFrame"] {
            margin-left: 0px !important;
            padding-left: 0px !important;
            width: 100% !important;
        }
        
        /* Main container - full viewport height */
        .main .block-container {
            padding: 0 !important;
            max-width: 100% !important;
        }
        
        /* Login container - full viewport height */
        .login-container {
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 0;
        }
        
        /* Input Fields Styling */
        .stTextInput > div > div > input {
            background-color: #0F1322 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
            padding: 12px 16px !important;
            color: #F9FAFB !important;
            transition: all 0.3s ease;
        }
        .stTextInput > div > div > input:focus {
            border-color: #7C3AED !important;
            box-shadow: 0 0 0 1px #7C3AED !important;
        }
        
        /* Labels Styling */
        .stTextInput label {
            color: #E5E7EB !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            padding-bottom: 4px;
        }

        /* Checkbox Styling */
        .stCheckbox p {
            color: #D1D5DB !important;
            font-size: 14px !important;
        }
        
        /* Button Styling */
        .stButton > button {
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px;
            padding: 12px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4);
        }
        /* Transparent button styling for Sign Up and Back to Login */
        div[data-testid="stVerticalBlock"] > div:has(> button[data-testid="baseButton-primary"]) > div > button:nth-of-type(2) { background: transparent !important; border: 1px solid rgba(167, 139, 250, 0.5) !important; color: white !important; box-shadow: none !important; } div[data-testid="stVerticalBlock"] > div:has(> button[data-testid="baseButton-primary"]) > div > button:nth-of-type(2):hover { background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important; border-color: transparent !important; }
        div[data-testid="stVerticalBlock"] > div:has(> button[data-testid="baseButton-primary"]) > div > button:nth-of-type(3) { background: transparent !important; border: 1px solid rgba(167, 139, 250, 0.5) !important; color: white !important; box-shadow: none !important; } div[data-testid="stVerticalBlock"] > div:has(> button[data-testid="baseButton-primary"]) > div > button:nth-of-type(3):hover { background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important; border-color: transparent !important; }
        
        /* Divider */
        .divider {
            display: flex;
            align-items: center;
            text-align: center;
            color: #6B7280;
            font-size: 14px;
            margin: 16px 0;
        }
        .divider::before, .divider::after {
            content: '';
            flex: 1;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        .divider::before { margin-right: 10px; }
        .divider::after { margin-left: 10px; }
        
        /* Branding Styles */
        .brand-title {
            font-size: 42px;
            font-weight: 700;
            color: #F9FAFB;
            line-height: 1.2;
            margin-bottom: 24px;
        }
        .highlight-text {
            background: linear-gradient(135deg, #A78BFA 0%, #7C3AED 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .feature-list {
            list-style: none;
            padding-left: 0;
            font-size: 18px;
            color: #E5E7EB;
            line-height: 2;
        }
        .feature-list li::before {
            content: '✓';
            color: #A78BFA;
            font-weight: bold;
            display: inline-block; 
            width: 1em;
            margin-left: -1em;
            border: 1px solid #A78BFA;
            border-radius: 50%;
            text-align: center;
            width: 20px;
            height: 20px;
            line-height: 20px;
            font-size: 12px;
            margin-right: 12px;
        }
        
        /* Auth Card Styling - Glassmorphism */
        .auth-card {
            background: rgba(11, 14, 23, 0.95);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(167, 139, 250, 0.15);
            border-radius: 18px;
            padding: 32px;
            box-shadow: 0 8px 32px rgba(167, 139, 250, 0.15), 0 4px 16px rgba(0, 0, 0, 0.3);
            width: 85%;
            max-width: 450px;
        }
        
        /* Responsive Design - Stack vertically on smaller screens */
        @media (max-width: 1024px) {
            .auth-card {
                width: 90%;
                max-width: 400px;
                padding: 24px;
            }
        }
        
        @media (max-width: 768px) {
            .auth-card {
                width: 95%;
                max-width: 100%;
                padding: 20px;
            }
            .brand-title {
                font-size: 32px;
            }
            .feature-list {
                font-size: 16px;
            }
        }
        
        /* Remove Streamlit default spacing */
        .stVerticalBlock {
            gap: 0.5rem !important;
        }
        
        /* Column gap - reduce space between 60% and 40% */
        [data-testid="stHorizontalBlock"] > [style*="flex-direction: row"] {
            gap: 0.6rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Creating the two-column layout - 60% left / 40% right
    col1, col2 = st.columns([0.6, 0.4])

    # --- LEFT COLUMN: Branding & Features ---
    with col1:
        st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 32px; padding-left: 10%;">
            <svg width="40" height="40" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-right: 12px;">
                <path d="M4 24V16h4v8H4zM12 24V8h4v16h-4zM20 24V12h4v12h-4z" fill="#A78BFA"/>
                <path d="M28 24V4h4v20h-4z" fill="#7C3AED"/>
            </svg>
            <h1 style="margin:0; font-size: 36px; font-weight: 600;">InSightX</h1>
        </div>
        
        <div class="brand-title" style="padding-left: 10%;">
            Turn Retail Data Into<br>
            <span class="highlight-text">Intelligent</span> Decisions
        </div>
        
        <ul class="feature-list" style="padding-left: 10%;">
            <li>AI Analytics</li>
            <li>Forecasting</li>
            <li>Recommendations</li>
            <li>Business Health</li>
        </ul>
        """, unsafe_allow_html=True)

    # --- RIGHT COLUMN: Authentication Form ---
    with col2:
        st.markdown('<div style="display: flex; justify-content: center; align-items: center; height: 100%; padding-left: 5%;">', unsafe_allow_html=True)
        
        # Login form container without auth card styling
        st.markdown('<div style="width: 85%; max-width: 450px;">', unsafe_allow_html=True)

        if st.session_state["auth_mode"] == "Login":
            st.markdown("""
                <h2 style="margin-bottom: 4px; color: #F9FAFB; font-size: 28px; font-weight: 600;">Login</h2>
                <p style="color: #9CA3AF; margin-bottom: 20px; font-size: 13px;">Welcome back! Please login to your account.</p>
            """, unsafe_allow_html=True)
            
            email = st.text_input("Email", placeholder="Enter your email", key="login_email")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
            
            # Remember me & Forgot Password Row
            c1, c2 = st.columns([1, 1])
            with c1:
                remember = st.checkbox("Remember me")
            with c2:
                st.markdown('<div style="text-align: right; margin-top: 8px;"><a href="#" style="color: #A78BFA; text-decoration: none; font-size: 14px;">Forgot Password?</a></div>', unsafe_allow_html=True)
            
            # Login Logic
            if st.button("Login →", use_container_width=True, key="login_btn"):
                login_user(email, password)
            
            st.markdown('<div class="divider">or</div>', unsafe_allow_html=True)
            
            # Switch to Sign Up
            st.markdown('<div style="margin-top: 0;">', unsafe_allow_html=True)
            st.markdown('<style>div[data-testid="stVerticalBlock"] > div:has(> button[data-testid="baseButton-primary"]) > div > button:nth-of-type(2) { background: transparent !important; border: 1px solid rgba(167, 139, 250, 0.5) !important; color: white !important; box-shadow: none !important; } div[data-testid="stVerticalBlock"] > div:has(> button[data-testid="baseButton-primary"]) > div > button:nth-of-type(2):hover { background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important; border-color: transparent !important; }</style>', unsafe_allow_html=True)
            if st.button("Sign Up", use_container_width=True):
                st.session_state["auth_mode"] = "Sign Up"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            # SIGN UP VIEW
            st.markdown("""
                <h2 style="margin-bottom: 4px; color: #F9FAFB; font-size: 28px; font-weight: 600;">Sign Up</h2>
                <p style="color: #9CA3AF; margin-bottom: 20px; font-size: 13px;">Create your account to get started.</p>
            """, unsafe_allow_html=True)
            
            full_name = st.text_input("Full Name", placeholder="Enter your full name", key="signup_name")
            email = st.text_input("Email", placeholder="Enter your email", key="signup_email")
            password = st.text_input("Password", type="password", placeholder="Create a password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="signup_confirm")
            
            # Sign Up Logic
            if st.button("Create Account →", use_container_width=True, key="signup_btn"):
                try:
                    if password != confirm_password:
                        st.error("❌ Passwords do not match")
                    else:
                        signup_user(email, password)
                except Exception as e:
                    st.error(f"❌ {str(e)}")
            
            st.markdown('<div class="divider">or</div>', unsafe_allow_html=True)
            
            # Switch to Login
            st.markdown('<div style="margin-top: 0;">', unsafe_allow_html=True)
            st.markdown('<style>div[data-testid="stVerticalBlock"] > div:has(> button[data-testid="baseButton-primary"]) > div > button:nth-of-type(3) { background: transparent !important; border: 1px solid rgba(167, 139, 250, 0.5) !important; color: white !important; box-shadow: none !important; } div[data-testid="stVerticalBlock"] > div:has(> button[data-testid="baseButton-primary"]) > div > button:nth-of-type(3):hover { background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important; border-color: transparent !important; }</style>', unsafe_allow_html=True)
            if st.button("Back to Login", use_container_width=True):
                st.session_state["auth_mode"] = "Login"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Powered by section below login form
        st.markdown('<div style="color: #6B7280; font-size: 9px; margin-top: 24px; text-align: center; white-space: nowrap;">', unsafe_allow_html=True)
        st.markdown('Powered by <span style="color: #E5E7EB;">🚀 Groq</span> <span style="color: #10B981;">⚡ Supabase</span> <span style="color: #EF4444;">👑 Streamlit</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Close login form container
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.stop() # Prevents the rest of the app from running until authenticated

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    /* Dark Mode Theme */
    :root {
        --bg-primary: #0B0F19;
        --bg-secondary: #111827;
        --bg-card: rgba(255, 255, 255, 0.06);
        --border-color: rgba(255, 255, 255, 0.08);
        --text-primary: #F9FAFB;
        --text-secondary: #9CA3AF;
        --primary: #4F46E5;
        --secondary: #7C3AED;
        --success: #10B981;
        --warning: #F59E0B;
        --danger: #EF4444;
    }
    
    .stApp {
        background-color: var(--bg-primary);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f35 0%, #0B0F19 100%);
        border-right: 1px solid rgba(79, 70, 229, 0.2);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
    }
    
    /* Sidebar Navigation Buttons */
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(79, 70, 229, 0.1) !important;
        border: 1px solid rgba(79, 70, 229, 0.2) !important;
        color: #E5E7EB !important;
        text-align: left !important;
        justify-content: flex-start !important;
        padding: 12px 16px !important;
        margin: 4px 0 !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
        border-color: transparent !important;
        transform: translateX(4px) !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
    }
    
    /* Sidebar button inner elements - force left alignment */
    [data-testid="stSidebar"] .stButton > button p,
    [data-testid="stSidebar"] .stButton > button div,
    [data-testid="stSidebar"] .stButton > button span {
        text-align: left !important;
        width: 100% !important;
    }
    
    /* Sidebar Collapse/Expand Button Styling */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="stSidebarCollapsedControl"] button,
    button[kind="header"] {
        opacity: 1 !important;
        visibility: visible !important;
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
        border: none !important;
        border-radius: 8px !important;
        color: white !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stSidebarCollapseButton"] button:hover,
    [data-testid="stSidebarCollapsedControl"] button:hover,
    button[kind="header"]:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 6px 16px rgba(79, 70, 229, 0.4) !important;
    }

    /* Ensure icons (SVGs) inside these buttons are white */
    [data-testid="stSidebarCollapseButton"] button svg,
    [data-testid="stSidebarCollapsedControl"] button svg {
        stroke: white !important;
        fill: white !important;
        color: white !important;
    }
    
    /* Completely Hide Radio Button Elements */
    [data-testid="stSidebar"] .stRadio {
        display: none !important;
    }
    
    [data-testid="stSidebar"] .stRadio > * {
        display: none !important;
    }
    
    /* Hide Streamlit's automatic page navigation in sidebar */
    [data-testid="stSidebar"] [data-testid="stSidebarNav"],
    [data-testid="stSidebar"] [data-testid="stSidebarNavItems"],
    [data-testid="stSidebar"] [data-testid="stSidebarNavContainer"],
    [data-testid="stSidebar"] .stSidebarNav,
    [data-testid="stSidebar"] section[data-testid="stSidebarNav"],
    [data-testid="stSidebar"] div[data-testid="stSidebarNav"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
        overflow: hidden !important;
    }
    
    /* Hide any navigation links in sidebar */
    [data-testid="stSidebar"] a[href*="dashboard"],
    [data-testid="stSidebar"] a[href*="analytics"],
    [data-testid="stSidebar"] a[href*="forecast"],
    [data-testid="stSidebar"] a[href*="anomaly"],
    [data-testid="stSidebar"] a[href*="recommendations"],
    [data-testid="stSidebar"] a[href*="business"],
    [data-testid="stSidebar"] a[href*="assistant"],
    [data-testid="stSidebar"] a[href*="reports"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Hide all links in sidebar that might be page navigation */
    [data-testid="stSidebar"] .stNavLink,
    [data-testid="stSidebar"] [data-testid="stNavLink"] {
        display: none !important;
    }
    
    /* Main Content */
    .main .block-container {
        background-color: var(--bg-primary);
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Hide any navigation tabs or radio buttons in main content */
    .main .stRadio {
        display: none !important;
    }
    
    .main [role="radiogroup"] {
        display: none !important;
    }
    
    .main .stTabs {
        display: none !important;
    }
    
    
    /* Headers */
    h1, h2, h3 {
        color: var(--text-primary) !important;
        font-weight: 600;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
    }
    
    /* Cards */
    .stCard {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(79, 70, 229, 0.3);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        color: var(--text-primary);
    }
    
    /* Dataframe */
    .stDataFrame {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
    }
    
    /* Plotly Charts */
    .js-plotly-plot {
        background: transparent;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-secondary);
    }
    
    /* Responsive Sticky Header */
    .sticky-header {
        position: sticky;
        top: 0;
        z-index: 999;
        background: rgba(11, 15, 25, 0.95);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding: 16px 24px;
        margin: -2rem -2rem 2rem -2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .header-right {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    
    .header-datetime {
        text-align: right;
    }
    
    /* Mobile Responsive View (< 768px) */
    @media (max-width: 768px) {
        .sticky-header {
            flex-direction: column;
            align-items: stretch;
            padding: 12px 16px;
            margin: -2rem -1rem 1.5rem -1rem;
            gap: 10px;
        }
        
        .header-left {
            justify-content: space-between;
            width: 100%;
        }
        
        .header-right {
            justify-content: space-between;
            width: 100%;
            gap: 12px;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            padding-top: 8px;
        }
        
        /* Hide datetime on mobile to save space */
        .header-datetime {
            display: none !important;
        }
        
        .header-left svg {
            width: 32px;
            height: 32px;
        }
        
        .header-left h1 {
            font-size: 16px !important;
        }
        
        .header-left p {
            font-size: 10px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:
    # Logo and branding
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 24px; padding: 16px;">
        <svg width="40" height="40" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" style="margin-right: 12px;">
            <path d="M4 24V16h4v8H4zM12 24V8h4v16h-4zM20 24V12h4v12h-4z" fill="#A78BFA"/>
            <path d="M28 24V4h4v20h-4z" fill="#7C3AED"/>
        </svg>
        <div>
            <h1 style="margin: 0; font-size: 20px; font-weight: 600; color: #F9FAFB;">InSightX</h1>
            <p style="margin: 0; color: #9CA3AF; font-size: 12px;">AI Retail Intelligence</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation using buttons
    pages = [
        ("Dashboard", "📊"),
        ("Analytics", "📈"),
        ("Forecast", "🔮"),
        ("Anomaly Detection", "⚠️"),
        ("AI Recommendations", "💡"),
        ("Business Health", "💪"),
        ("AI Assistant", "🤖"),
        ("Reports", "📄")
    ]
    
    current_page = st.session_state.get("page", "Dashboard")
    
    for page_name, icon in pages:
        if st.button(f"{icon} {page_name}", key=f"nav_{page_name}", use_container_width=True):
            st.session_state["page"] = page_name
            st.rerun()
    
    st.markdown("---")
    
    # User info
    st.markdown("### User Info")
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.15) 0%, rgba(124, 58, 237, 0.1) 100%);
        border: 1px solid rgba(79, 70, 229, 0.3);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
    ">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="
                width: 40px;
                height: 40px;
                background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
            ">👤</div>
            <div>
                <div style="color: #F9FAFB; font-size: 14px; font-weight: 600;">{st.session_state["user"]}</div>
                <div style="color: #9CA3AF; font-size: 12px;">{'✨ Premium' if st.session_state.get('is_paid', False) else 'Free User'}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    if st.session_state["df"] is not None:
        df = st.session_state["df"]
        num_cols = df.select_dtypes(include="number").columns
        total_sales = df[num_cols[0]].sum() if len(num_cols) > 0 else 0
        total_records = len(df)
        
        st.markdown(f"""
        <div style="padding: 16px; background: rgba(255, 255, 255, 0.03); border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.06);">
            <p style="color: #6B7280; margin: 0 0 8px 0; font-size: 11px; font-weight: 500; letter-spacing: 0.5px;">QUICK STATS</p>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #9CA3AF; font-size: 12px;">Records</span>
                <span style="color: #F9FAFB; font-size: 12px; font-weight: 600;">{total_records:,}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #9CA3AF; font-size: 12px;">Total Sales</span>
                <span style="color: #F9FAFB; font-size: 12px; font-weight: 600;">${total_sales:,.0f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Logout button
    if st.button("Logout", use_container_width=True):
        logout_user()

# ================= TOAST / NOTIFICATION =================
if st.session_state.get("show_success_toast", False):
    st.toast("Welcome to InSightX Premium. Enjoy all AI-powered retail intelligence features.", icon="👑")
    st.success("✅ Premium Access Unlocked! Welcome to InSightX Premium.")
    st.session_state["show_success_toast"] = False

# ================= FILE UPLOADER / PAYWALL =================
if st.session_state["is_paid"]:
    file = st.file_uploader("Upload CSV")
    if file:
        df = pd.read_csv(file, encoding='latin1')
        df.columns = df.columns.str.lower()
        st.session_state["df"] = df
else:
    st.info("🔒 Custom file upload is locked in Demo Mode. Upgrade to Premium to upload your own custom CSV datasets.")

if st.session_state["df"] is None:
    st.stop()

df = st.session_state["df"]

# ================= STICKY HEADER =================
badge_or_button_html = ""
if st.session_state["is_paid"]:
    badge_or_button_html = '<span style="background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%); color: white; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; box-shadow: 0 0 10px rgba(245, 158, 11, 0.5); display: inline-flex; align-items: center; gap: 4px; margin-right: 12px;">👑 Premium</span>'
else:
    badge_or_button_html = '<a href="/?page=premium" target="_self" style="text-decoration: none; background: linear-gradient(135deg, #7C3AED 0%, #4F46E5 100%); color: white; padding: 8px 16px; border-radius: 8px; font-weight: 600; font-size: 14px; box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3); margin-right: 12px;">⭐ Upgrade to Premium</a>'

st.markdown(f"""
<div class="sticky-header">
    <div class="header-left">
        <svg width="36" height="36" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M4 24V16h4v8H4zM12 24V8h4v16h-4zM20 24V12h4v12h-4z" fill="#A78BFA"/>
            <path d="M28 24V4h4v20h-4z" fill="#7C3AED"/>
        </svg>
        <div>
            <h1 style="margin: 0; color: #F9FAFB; font-size: 18px; font-weight: 600;">InSightX Dashboard</h1>
            <p style="margin: 2px 0 0 0; color: #9CA3AF; font-size: 11px;">AI Retail Intelligence Platform</p>
        </div>
    </div>
    <div class="header-right">
        {badge_or_button_html}
        <div class="header-datetime">
            <p style="margin: 0; color: #F9FAFB; font-size: 13px; font-weight: 500;">{datetime.now().strftime("%B %d, %Y")}</p>
            <p style="margin: 0; color: #9CA3AF; font-size: 11px;">{datetime.now().strftime("%I:%M %p")}</p>
        </div>
        <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #10B981 0%, #059669 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0;">👤</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Demo Mode top banner
if not st.session_state["is_paid"]:
    st.info("🚀 Demo Mode — Explore InSightX with limited functionality. Upgrade to Premium for full AI capabilities.")

num_cols = df.select_dtypes(include="number").columns
cat_cols = df.select_dtypes(include="object").columns

# ================= PAGE ROUTING =================
current_page = st.session_state.get("page", "Dashboard")

if current_page == "Dashboard":
    render_dashboard(df, num_cols, cat_cols)
elif current_page == "Analytics":
    render_analytics(df, num_cols, cat_cols)
elif current_page == "Forecast":
    render_forecast(df, num_cols)
elif current_page == "Anomaly Detection":
    render_anomaly_detection(df, num_cols)
elif current_page == "AI Recommendations":
    render_recommendations(df, num_cols, cat_cols)
elif current_page == "Business Health":
    render_business_health(df, num_cols, cat_cols)
elif current_page == "AI Assistant":
    render_ai_assistant(df, num_cols, cat_cols)
elif current_page == "Reports":
    # Calculate totals for reports
    total_sales = df[num_cols[0]].sum() if len(num_cols) > 0 else 0
    total_profit = df[num_cols[1]].sum() if len(num_cols) > 1 else 0
    # Charts would need to be generated and passed here
    charts = []  # Placeholder for charts
    render_reports(df, num_cols, cat_cols, total_sales, total_profit, charts)
