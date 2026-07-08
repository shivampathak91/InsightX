import streamlit as st
from ai_functions import generate_recommendations
from ui_components import create_premium_card, create_chart_container

def render_recommendations(df, num_cols, cat_cols):
    """Render the AI Recommendations page"""
    create_chart_container("AI Recommendation Engine", "Actionable business insights", icon="💡")

    with st.expander("Get Actionable Business Recommendations", expanded=True):
        st.info("AI analyzes your data to generate prioritized business recommendations.")
        
        if st.button("Generate Recommendations", key="rec_btn_page"):
            with st.spinner("Analyzing data and generating recommendations..."):
                recommendations = generate_recommendations(df, num_cols, cat_cols)
                create_premium_card("AI-Powered Business Recommendations", recommendations.replace('\n', '<br/>'), icon="💡", color="green")
