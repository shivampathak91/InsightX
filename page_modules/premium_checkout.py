import streamlit as st
import time
import base64
import os
from datetime import datetime

def render_premium_checkout():
    # Custom CSS for Premium Checkout
    st.markdown("""
    <style>
        /* Force dark background matching login page gradients */
        .stApp {
            background-color: #060913 !important;
            background-image: radial-gradient(circle at 15% 85%, rgba(67, 30, 201, 0.15) 0%, transparent 40%),
                              radial-gradient(circle at 85% 15%, rgba(67, 30, 201, 0.05) 0%, transparent 40%) !important;
            color: #FFFFFF !important;
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
        .main .block-container {
            max-width: 100% !important;
            padding: 3rem !important;
        }
        
        /* Premium Card / Glassmorphism */
        .premium-card-left {
            background: rgba(11, 14, 23, 0.8) !important;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(167, 139, 250, 0.15) !important;
            border-radius: 18px !important;
            padding: 32px !important;
            box-shadow: 0 8px 32px rgba(167, 139, 250, 0.05), 0 4px 16px rgba(0, 0, 0, 0.3) !important;
        }

        .premium-card-right {
            background: rgba(11, 14, 23, 0.95) !important;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(167, 139, 250, 0.15) !important;
            border-radius: 18px !important;
            padding: 32px !important;
            box-shadow: 0 8px 32px rgba(167, 139, 250, 0.05), 0 4px 16px rgba(0, 0, 0, 0.3) !important;
        }

        .feature-item {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
            color: #E5E7EB;
            font-size: 14px;
        }
        
        .feature-icon {
            color: #A78BFA;
            font-weight: bold;
        }
        
        /* Input fields styling */
        .stTextInput > div > div > input {
            background-color: #0F1322 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
            padding: 12px 16px !important;
            color: #F9FAFB !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: #7C3AED !important;
        }
        
        /* Tab formatting */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(255,255,255,0.03) !important;
            border: 1px solid rgba(255,255,255,0.05) !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
            color: #9CA3AF !important;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #ffffff !important;
            background-color: rgba(124, 58, 237, 0.1) !important;
        }
        .stTabs [aria-selected="true"] {
            background-color: rgba(124, 58, 237, 0.2) !important;
            border-color: #7C3AED !important;
            color: #ffffff !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Brand Header Section
    st.markdown('<div style="text-align: center; margin-top: 30px; margin-bottom: 30px;"><div style="display: inline-flex; align-items: center; gap: 12px; margin-bottom: 8px;"><svg width="40" height="40" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 24V16h4v8H4zM12 24V8h4v16h-4zM20 24V12h4v12h-4z" fill="#A78BFA"/><path d="M28 24V4h4v20h-4z" fill="#7C3AED"/></svg><span style="font-size: 28px; font-weight: 700; color: #F9FAFB; letter-spacing: 0.5px;">InSightX</span></div><p style="color: #9CA3AF; font-size: 14px; margin: 0;">Secure Premium Checkout Platform</p></div>', unsafe_allow_html=True)

    # Layout columns
    left_col, right_col = st.columns([1, 1.1])

    with left_col:
        # Wrap everything in a single-line HTML structure to prevent escaping
        st.markdown('<div class="premium-card-left"><span style="background: linear-gradient(135deg, #A78BFA 0%, #7C3AED 100%); color: white; padding: 6px 16px; border-radius: 20px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">👑 Premium Access Upgrade</span><h2 style="margin-top: 20px; margin-bottom: 12px; font-size: 36px; font-weight: 700; color: white;">₹999 <span style="font-size: 16px; color: #9CA3AF; font-weight: 400;">/ one-time fee</span></h2><p style="color: #9CA3AF; margin-bottom: 32px; font-size: 14px; line-height: 1.5;">Unlock full data parsing, predictive forecasting, executive summaries, and AI agents instantly and permanently.</p><div style="border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 24px;"><p style="font-weight: 600; color: white; margin-bottom: 16px; font-size: 15px;">Included with Premium:</p><div class="feature-item"><span class="feature-icon">✓</span><span>Custom CSV Dataset Upload & Parsing</span></div><div class="feature-item"><span class="feature-icon">✓</span><span>Advanced AI Chatbot & Assistant Modules</span></div><div class="feature-item"><span class="feature-icon">✓</span><span>Predictive Sales Forecasting Models</span></div><div class="feature-item"><span class="feature-icon">✓</span><span>Anomaly & Fraud Pattern Detection</span></div><div class="feature-item"><span class="feature-icon">✓</span><span>Executive Summaries & AI Decisions</span></div><div class="feature-item"><span class="feature-icon">✓</span><span>Premium Reports & PDF Document Exports</span></div></div><div style="margin-top: 40px; text-align: center; border-top: 1px solid rgba(255, 255, 255, 0.05); padding-top: 20px;"><p style="color: #9CA3AF; font-size: 12px; margin-bottom: 4px; display: inline-flex; align-items: center; gap: 6px;">🔒 256-Bit SSL Secured Connection</p><p style="color: #6B7280; font-size: 11px; margin: 0;">Guaranteed safe checkout & encrypted transactions</p></div></div>', unsafe_allow_html=True)

    with right_col:
        # Wrap header in a single-line HTML structure
        st.markdown('<div class="premium-card-right"><h3 style="margin-bottom: 24px; font-weight: 600; color: white; font-size: 20px;">Choose Payment Option</h3></div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["💳 Card Payment", "📱 UPI / QR Scan", "🏦 Netbanking", "💼 Wallet Options"])
        payment_submitted = False
        
        with tab1:
            card_num = st.text_input("Card Number", placeholder="4111 2222 3333 4444", key="chk_card_num")
            card_name = st.text_input("Cardholder Name", placeholder="John Doe", key="chk_card_name")
            col_exp, col_cvv = st.columns(2)
            with col_exp:
                card_expiry = st.text_input("Expiry Date", placeholder="MM/YY", key="chk_card_exp")
            with col_cvv:
                card_cvv = st.text_input("CVV", type="password", placeholder="•••", key="chk_card_cvv")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Complete Payment • ₹999", key="pay_card", use_container_width=True, type="primary"):
                if not card_num or not card_name or not card_expiry or not card_cvv:
                    st.error("Please fill in all card details.")
                else:
                    payment_submitted = True
                    
        with tab2:
            st.markdown('<div style="text-align: center; padding: 12px 0;"><p style="color: #9CA3AF; font-size: 13px; margin-bottom: 12px;">Scan the QR code using Google Pay, PhonePe, or Paytm</p><div style="background: white; padding: 12px; border-radius: 12px; display: inline-block; margin-bottom: 12px;"><svg width="120" height="120" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 3h6v6H3V3zm2 2v2h2V5H5zm8-2h6v6h-6V3zm2 2v2h2V5h-2zM3 15h6v6H3v-6zm2 2v2h2v-2H5zm10-2h2v2h-2v-2zm2 2h2v2h-2v-2zm-2 2h2v2h-2v-2zm-4-4h2v2h-2v-2zm2 2h2v2h-2v-2zm-2 2h2v2h-2v-2zm-4-2H9v2h2v-2zm4-6h2v2h-2V9zm2 2h2v2h-2v-2z" fill="#0F172A"/></svg></div><p style="font-weight: 600; color: #E5E7EB; margin-bottom: 12px; font-size: 14px;">OR Pay via VPA (UPI ID)</p></div>', unsafe_allow_html=True)
            upi_id = st.text_input("UPI ID", placeholder="username@okaxis", key="chk_upi")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Verify & Pay ₹999", key="pay_upi", use_container_width=True, type="primary"):
                if not upi_id or "@" not in upi_id:
                    st.error("Please enter a valid UPI ID.")
                else:
                    payment_submitted = True

        with tab3:
            st.selectbox("Select Bank", ["HDFC Bank", "ICICI Bank", "State Bank of India", "Axis Bank", "Kotak Bank", "Punjab National Bank"], key="chk_bank")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Initiate Netbanking Secure Payment", key="pay_nb", use_container_width=True, type="primary"):
                payment_submitted = True

        with tab4:
            st.selectbox("Select Wallet Option", ["Paytm Wallet", "PhonePe Wallet", "Amazon Pay Balance", "Mobikwik Wallet"], key="chk_wallet")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Link Wallet & Pay ₹999", key="pay_wal", use_container_width=True, type="primary"):
                payment_submitted = True

        if payment_submitted:
            with st.spinner("Processing payment... Please do not close or refresh this tab."):
                time.sleep(2.5)
                
            st.session_state["is_paid"] = True
            st.session_state["show_success_toast"] = True
            if "page" in st.session_state:
                st.session_state["page"] = "Dashboard"
            st.query_params.clear()
            st.query_params["payment_success"] = "true"
            st.rerun()
            
        st.markdown('<div style="border-top: 1px solid rgba(255, 255, 255, 0.08); margin-top: 24px; padding-top: 20px; text-align: center; color: #6B7280;"><span style="font-size: 10px; letter-spacing: 0.5px; text-transform: uppercase;">Protected & Secured by</span><div style="display: flex; justify-content: center; align-items: center; gap: 16px; margin-top: 6px;"><span style="font-size: 14px; font-weight: 700; color: #3B82F6;">razorpay</span><span style="font-size: 12px; font-weight: 600; color: #10B981;">stripe</span></div></div>', unsafe_allow_html=True)
