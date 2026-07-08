import streamlit as st

# Inject CSS to hide sidebar immediately
st.markdown("""
<style>
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
</style>
""", unsafe_allow_html=True)

from page_modules.premium_checkout import render_premium_checkout

render_premium_checkout()
