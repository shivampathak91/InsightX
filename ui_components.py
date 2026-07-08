import streamlit as st
import plotly.graph_objects as go

def create_gauge_chart(score):
    """Create a gauge chart for health score"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        title = {'text': "Business Health Score"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 40], 'color': "lightgray"},
                {'range': [40, 70], 'color': "gray"},
                {'range': [70, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(height=300)
    return fig

def create_premium_card(title, content, icon="📊", color="blue"):
    """Create a premium dashboard card"""
    color_map = {
        "blue": "#4F46E5",
        "green": "#10B981",
        "red": "#EF4444",
        "orange": "#F59E0B",
        "purple": "#7C3AED"
    }
    bg_color = color_map.get(color, "#4F46E5")
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.1) 0%, rgba(124, 58, 237, 0.15) 100%);
        border-left: 4px solid {bg_color};
        padding: 24px;
        border-radius: 16px;
        margin: 16px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
    ">
        <h3 style="margin: 0 0 12px 0; color: {bg_color}; font-size: 18px; font-weight: 600;">{icon} {title}</h3>
        <div style="color: #E5E7EB; line-height: 1.6; white-space: pre-wrap;">{content}</div>
    </div>
    """, unsafe_allow_html=True)

def create_chart_container(title, description, icon="📊"):
    """Create a container for charts with title and description"""
    st.markdown(f"""
    <div style="
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    ">
        <div style="display: flex; align-items: center; margin-bottom: 16px;">
            <span style="font-size: 24px; margin-right: 12px;">{icon}</span>
            <div>
                <h3 style="margin: 0; color: #F9FAFB; font-size: 18px; font-weight: 600;">{title}</h3>
                <p style="margin: 4px 0 0 0; color: #9CA3AF; font-size: 13px;">{description}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
