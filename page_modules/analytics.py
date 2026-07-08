import streamlit as st
import plotly.express as px
from ai_functions import ai_explain
from ui_components import create_chart_container

def render_analytics(df, num_cols, cat_cols):
    """Render the Analytics page"""
    # Correlation Matrix
    create_chart_container("Correlation Matrix", "Relationship between numeric variables", icon="📉")
    corr_fig = None
    if len(num_cols) > 1:
        corr = df[num_cols].corr()
        corr_fig = px.imshow(corr)
        st.plotly_chart(corr_fig)

        if st.button("Explain Correlation", key="corr_btn_analytics"):
            st.info(ai_explain("Correlation matrix", corr.to_string()))

    # Sales vs Profit Scatter Plot
    create_chart_container("Sales vs Profit", "Scatter plot analysis", icon="💰")
    sv_fig = None
    if len(cat_cols) > 0 and len(num_cols) >= 2:
        seg = df.groupby(cat_cols[0])[[num_cols[0], num_cols[1]]].sum().reset_index()
        sv_fig = px.scatter(seg, x=num_cols[0], y=num_cols[1], color=cat_cols[0])
        st.plotly_chart(sv_fig)

        if st.button("Explain Sales vs Profit", key="seg_btn_analytics"):
            st.info(ai_explain("Sales vs profit scatter", seg.to_string()))
