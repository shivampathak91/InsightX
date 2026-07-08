import streamlit as st
from ai_functions import ai_explain

def render_ai_assistant(df, num_cols, cat_cols):
    """Render the AI Assistant page"""
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.1) 0%, rgba(124, 58, 237, 0.15) 100%);
        border: 1px solid rgba(79, 70, 229, 0.3);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    ">
        <div style="display: flex; align-items: center; margin-bottom: 16px;">
            <span style="font-size: 24px; margin-right: 12px;">🤖</span>
            <div>
                <h3 style="margin: 0; color: #F9FAFB; font-size: 18px; font-weight: 600;">AI Chatbot</h3>
                <p style="margin: 4px 0 0 0; color: #9CA3AF; font-size: 13px;">Ask questions about your data</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # store chat history
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Chat container styling
    st.markdown("""
    <style>
        .chat-container {
            max-height: 400px;
            overflow-y: auto;
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 16px;
        }
        .user-message {
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
            color: white;
            padding: 12px 16px;
            border-radius: 12px 12px 0 12px;
            margin-bottom: 12px;
            max-width: 80%;
            margin-left: auto;
        }
        .ai-message {
            background: rgba(255, 255, 255, 0.1);
            color: #E5E7EB;
            padding: 12px 16px;
            border-radius: 12px 12px 12px 0;
            margin-bottom: 12px;
            max-width: 80%;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        /* Align send button with input */
        [data-testid="stForm"] [data-testid="stHorizontalBlock"] > div {
            align-items: flex-end !important;
        }
        [data-testid="stForm"] [data-testid="stHorizontalBlock"] > div > div > button {
            height: 52px !important;
            margin-top: 0 !important;
        }
        [data-testid="stForm"] [data-testid="stHorizontalBlock"] > div > div:first-child > div > div {
            padding-top: 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Display chat history with bubbles
    for role, msg in st.session_state["chat_history"]:
        if role == "You":
            st.markdown(f"""
            <div class="user-message">
                <strong>🧑 You:</strong><br/>{msg}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="ai-message">
                <strong>🤖 AI:</strong><br/>{msg}
            </div>
            """, unsafe_allow_html=True)

    # Input area
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            user_query = st.text_input(
                "",
                placeholder="Type your question here...",
                key="chat_input",
                label_visibility="collapsed"
            )
        with col2:
            ask_button = st.form_submit_button("Send", use_container_width=True)
        
        if ask_button and user_query:
            # 🔥 CONTEXT FOR AI
            context = f"""
Columns: {list(df.columns)}

Sample Data:
{df.head(5).to_string()}

Stats:
{df.describe().to_string()}
"""

            answer = ai_explain(user_query, context)

            # save history
            st.session_state["chat_history"].append(("You", user_query))
            st.session_state["chat_history"].append(("AI", answer))
            st.rerun()
